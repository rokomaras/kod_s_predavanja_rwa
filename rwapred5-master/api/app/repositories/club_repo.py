# =============================================================
# club_repo.py — DB upiti za Club model
# =============================================================

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.club import Club


async def get_all(db: AsyncSession) -> list[Club]:
    """Dohvati sve klubove s eagerly loaded users relacijom."""
    result = await db.execute(
        select(Club).options(selectinload(Club.users)).order_by(Club.id)
    )
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, club_id: int) -> Club | None:
    """Dohvati klub po ID-u s users relacijom."""
    result = await db.execute(
        select(Club).options(selectinload(Club.users)).where(Club.id == club_id)
    )
    return result.scalar_one_or_none()


async def get_by_name(db: AsyncSession, name: str) -> Club | None:
    """Dohvati klub po imenu (za provjeru duplikata)."""
    result = await db.execute(select(Club).where(Club.name == name))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, club: Club) -> Club:
    """Spremi novi klub u bazu."""
    db.add(club)
    await db.flush()
    return club
