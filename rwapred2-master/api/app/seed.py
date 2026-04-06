# =============================================================
# seed.py — Inicijalni podaci za razvoj i testiranje
# =============================================================
# Kreira admin korisnika, dva demo kluba i njihove korisnike.
#
# Pokretanje (iz api/ direktorija):
#   python -m app.seed
#
# Zašto seed?
#   - Nakon "alembic upgrade head" imamo prazne tablice
#   - Za razvoj trebamo barem admin login i klubove
#   - Za testiranje auth/ownership logike (predavanje 3-4)
#     trebamo dva kluba da dokažemo da jedan ne vidi drugog
#
# Idempotentnost:
#   Skripta provjerava postoji li već zapis s istim username/imenom.
#   Ako postoji — preskače. Sigurno je pokrenuti višestruko.
# =============================================================

import asyncio
import logging

import bcrypt as _bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal, engine
from app.models.club import Club
from app.models.user import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---- Seed podaci ------------------------------------------------
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

CLUBS = [
    {
        "name": "Behemot",
        "city": "Zadar",
        "contact_email": "behemot@example.com",
        "contact_phone": "+385 23 555 111",
        "username": "behemot",
        "password": "klub123",
    },
    {
        "name": "Bolest",
        "city": "Split",
        "contact_email": "bolest@example.com",
        "contact_phone": "+385 21 555 222",
        "username": "bolest",
        "password": "klub123",
    },
]


def _hash_pw(plain: str) -> str:
    return _bcrypt.hashpw(plain.encode(), _bcrypt.gensalt()).decode()


async def _seed_club(session: AsyncSession, data: dict) -> Club:
    """Kreiraj klub i pripadajućeg club usera ako ne postoje."""
    result = await session.execute(select(Club).where(Club.name == data["name"]))
    club = result.scalar_one_or_none()

    if club is None:
        club = Club(
            name=data["name"],
            city=data["city"],
            contact_email=data.get("contact_email"),
            contact_phone=data.get("contact_phone"),
        )
        session.add(club)
        await session.flush()
        logger.info("Kreiran klub: %s (id=%s)", club.name, club.id)
    else:
        logger.info("Klub '%s' već postoji — preskačem.", club.name)

    result = await session.execute(
        select(User).where(User.username == data["username"])
    )
    if result.scalar_one_or_none() is None:
        user = User(
            username=data["username"],
            password_hash=_hash_pw(data["password"]),
            role="club",
            club_id=club.id,
        )
        session.add(user)
        logger.info("Kreiran club user: %s (club=%s)", user.username, club.name)

    return club


async def seed(session: AsyncSession) -> None:
    """
    Kreira inicijalne podatke ako ne postoje.

    Redoslijed: klubovi prvo (jer user treba club_id), pa admin.
    """

    # -- 1. Klubovi + njihovi korisnici --
    for club_data in CLUBS:
        await _seed_club(session, club_data)

    # -- 2. Admin user --
    result = await session.execute(
        select(User).where(User.username == ADMIN_USERNAME)
    )
    if result.scalar_one_or_none() is None:
        admin = User(
            username=ADMIN_USERNAME,
            password_hash=_hash_pw(ADMIN_PASSWORD),
            role="admin",
            club_id=None,
        )
        session.add(admin)
        logger.info("Kreiran admin: %s", admin.username)

    await session.commit()
    logger.info("Seed završen uspješno!")


async def main() -> None:
    """Entry point — otvara sesiju, pokreće seed, zatvara engine."""
    async with AsyncSessionLocal() as session:
        await seed(session)
    # Čisto zatvaranje svih konekcija u poolu.
    await engine.dispose()


# Omogućuje pokretanje sa: python -m app.seed
if __name__ == "__main__":
    asyncio.run(main())

