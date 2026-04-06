# =============================================================
# registration_repo.py — DB upiti za Registration model
# =============================================================

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.registration import Registration


async def get_by_competition(
    db: AsyncSession,
    comp_id: int,
    club_id: int | None = None,
) -> list[Registration]:
    """
    Prijave za natjecanje.
    Ako je club_id dan, filtrira samo prijave liftera tog kluba.
    """
    stmt = (
        select(Registration)
        .options(selectinload(Registration.lifter))
        .where(Registration.competition_id == comp_id)
    )
    if club_id is not None:
        from app.models.lifter import Lifter
        stmt = stmt.join(Lifter).where(Lifter.club_id == club_id)
    stmt = stmt.order_by(Registration.id)
    result = await db.execute(stmt)
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, reg_id: int) -> Registration | None:
    """Dohvati prijavu po ID-u s lifter relacijom."""
    result = await db.execute(
        select(Registration)
        .options(selectinload(Registration.lifter))
        .where(Registration.id == reg_id)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, registration: Registration) -> Registration:
    """Spremi novu prijavu."""
    db.add(registration)
    await db.flush()
    return registration
