# =============================================================
# deps.py — Zajedničke FastAPI dependencije
# =============================================================
# FastAPI koristi Dependency Injection (DI) sustav:
# endpoint deklarira ŠTO treba, a framework KAKO to dobiti.
#
# Primjer (dolazi u predavanju 2-3):
#   async def get_db() -> AsyncGenerator[AsyncSession, None]:
#       async with SessionLocal() as session:
#           yield session
#
#   @router.get("/lifters")
#   def list_lifters(db: AsyncSession = Depends(get_db)):
#       ...
#
# Prednosti DI-ja:
#   - Endpoint ne zna kako se kreira DB sesija
#   - U testovima možemo podmetnuti mock sesiju
#   - Resursi se automatski zatvaraju nakon requesta
#
# Za sada prazan — popunjavamo u sljedećim predavanjima.
# =============================================================
