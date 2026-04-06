# =============================================================
# deps.py — Zajedničke FastAPI dependencije
# =============================================================
# FastAPI koristi Dependency Injection (DI) sustav:
# endpoint deklarira ŠTO treba, a framework KAKO to dobiti.
#
# Primjer korištenja u routeru:
#   @router.get("/clubs")
#   async def list_clubs(db: AsyncSession = Depends(get_db)):
#       result = await db.execute(select(Club))
#       return result.scalars().all()
#
# Prednosti DI-ja:
#   - Endpoint ne zna kako se kreira DB sesija
#   - U testovima možemo podmetnuti mock sesiju
#   - Resursi se automatski zatvaraju nakon requesta
# =============================================================

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency koja daje DB sesiju za svaki request.

    Tijek:
      1. Kreira novu async sesiju
      2. yield → endpoint je koristi (SELECT, INSERT, …)
      3. Ako nema iznimke → commit (spremanje promjena)
      4. Ako je iznimka → rollback (poništavanje)
      5. finally → sesija se zatvara (vraća konekciju u pool)

    Zašto session-per-request?
      - Svaki request ima izoliranu transakciju
      - Nema "curenja" stanja između dva paralelna requesta
      - Automatski cleanup — nema zaboravljenih otvorenih konekcija
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
