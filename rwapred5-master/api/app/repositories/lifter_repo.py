# =============================================================
# lifter_repo.py — DB upiti za Lifter model
# =============================================================

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lifter import Lifter


async def get_by_club(
    db: AsyncSession,
    club_id: int,
    gender: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Lifter]:
    """Lista natjecatelja kluba s opcionalnim filterom i paginacijom."""
    stmt = select(Lifter).where(Lifter.club_id == club_id)
    if gender is not None:
        stmt = stmt.where(Lifter.gender == gender)
    stmt = stmt.order_by(Lifter.id).limit(limit).offset(offset)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, lifter_id: int) -> Lifter | None:
    """Dohvati natjecatelja po ID-u."""
    result = await db.execute(select(Lifter).where(Lifter.id == lifter_id))
    return result.scalar_one_or_none()


async def create(db: AsyncSession, lifter: Lifter) -> Lifter:
    """Spremi novog natjecatelja."""
    db.add(lifter)
    await db.flush()
    return lifter


async def delete(db: AsyncSession, lifter: Lifter) -> None:
    """Obriši natjecatelja."""
    await db.delete(lifter)
