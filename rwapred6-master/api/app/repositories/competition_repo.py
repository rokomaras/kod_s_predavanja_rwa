# =============================================================
# competition_repo.py — DB upiti za Competition model
# =============================================================

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.competition import Competition


async def get_all(db: AsyncSession) -> list[Competition]:
    """Dohvati sva natjecanja, sortirana po datumu."""
    result = await db.execute(select(Competition).order_by(Competition.date))
    return list(result.scalars().all())


async def get_by_id(db: AsyncSession, comp_id: int) -> Competition | None:
    """Dohvati natjecanje po ID-u."""
    result = await db.execute(
        select(Competition).where(Competition.id == comp_id)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, competition: Competition) -> Competition:
    """Spremi novo natjecanje."""
    db.add(competition)
    await db.flush()
    return competition
