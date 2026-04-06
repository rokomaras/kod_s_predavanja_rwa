# Označava "repositories" kao Python paket.
# Ovdje žive DB upiti — SQL logika izolirana od poslovnih pravila.
# Repository prima SQLAlchemy session i vraća domenske objekte.
# Primjer (dolazi u predavanju 5):
#   async def get_lifters_by_club(db: AsyncSession, club_id: int) -> list[Lifter]:
#       result = await db.execute(select(Lifter).where(...))
#       return result.scalars().all()
