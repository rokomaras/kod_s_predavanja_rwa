# =============================================================
# conftest.py — Test infrastruktura (fixtures i DB setup)
# =============================================================
# Koristimo in-memory SQLite umjesto PostgreSQL-a za testove:
#   - Brzo (nema mrežnih poziva)
#   - Nema ovisnosti o Dockeru
#   - Svaki test dobije čistu bazu (izolacija)
#
# StaticPool osigurava da sve async sesije dijele istu
# in-memory bazu (inače bi svaka konekcija dobila svoju).
# =============================================================

from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from app.core.database import Base
from app.core.deps import get_db
from app.core.security import hash_password
from app.main import app as fastapi_app
from app.models.club import Club
from app.models.user import User

# --- Test engine (SQLite in-memory) ---

engine_test = create_async_engine(
    "sqlite+aiosqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestSessionLocal = async_sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)


# --- Dependency override ---

async def _override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


fastapi_app.dependency_overrides[get_db] = _override_get_db


# --- Fixtures ---

@pytest.fixture(autouse=True)
async def setup_database():
    """Kreira tablice prije testa, briše ih nakon — potpuna izolacija."""
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db() -> AsyncGenerator[AsyncSession, None]:
    """Sesija za seeding test podataka u fixtureima."""
    async with TestSessionLocal() as session:
        yield session


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP klijent za testiranje endpointova."""
    transport = ASGITransport(app=fastapi_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def admin_user(db: AsyncSession) -> User:
    """Admin korisnik za testove (username=testadmin, password=admin123)."""
    user = User(
        username="testadmin",
        password_hash=hash_password("admin123"),
        role="admin",
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@pytest.fixture
async def club_and_user(db: AsyncSession) -> tuple[Club, User]:
    """Club + club user za testove (username=testclub, password=klub123)."""
    club = Club(name="TestClub", city="TestCity")
    db.add(club)
    await db.flush()

    user = User(
        username="testclub",
        password_hash=hash_password("klub123"),
        role="club",
        club_id=club.id,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    await db.refresh(club)
    return club, user


@pytest.fixture
async def inactive_user(db: AsyncSession) -> User:
    """Deaktivirani korisnik za testiranje is_active provjere."""
    user = User(
        username="inactive",
        password_hash=hash_password("pass123"),
        role="admin",
        is_active=False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def auth_header(client: AsyncClient, username: str, password: str) -> dict:
    """Helper: napravi login i vrati Authorization header dict."""
    resp = await client.post("/auth/login", json={"username": username, "password": password})
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
