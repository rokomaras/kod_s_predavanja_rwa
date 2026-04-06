# =============================================================
# database.py — SQLAlchemy engine, session factory i Base model
# =============================================================
# Ovo je "infrastrukturni" modul — postavlja KAKO se spajamo
# na bazu i KAKO kreiramo sesije. Modeli (tablice) se definiraju
# u app/models/, a ovaj modul im daje Base klasu.
#
# Tri ključna koncepta:
#   1. Engine   — pool konekcija prema bazi (async)
#   2. Session  — "razgovor" s bazom unutar jednog requesta
#   3. Base     — bazna klasa iz koje nasljeđuju svi ORM modeli
#
# Korištenje u ostatku koda:
#   from app.core.database import Base          # za modele
#   from app.core.database import AsyncSessionLocal  # za deps.py
# =============================================================

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

# 1. Engine — async konekcija prema PostgreSQL-u.
#    create_async_engine koristi asyncpg driver (definiran u DATABASE_URL).
#    pool_pre_ping=True: prije svake konekcije iz poola pošalje "ping"
#    da provjeri je li konekcija još živa (sprječava "connection closed" greške).
engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

# 2. Session factory — "tvornica" za kreiranje sesija.
#    async_sessionmaker vraća klasu (ne instancu!) koja kreira sesije.
#    expire_on_commit=False: nakon commita, objekti ostaju dostupni
#    bez ponovnog querya (korisno za vraćanje podataka u API odgovorima).
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# 3. Base — deklarativna bazna klasa za sve ORM modele.
#    Svaki model koji nasljeđuje Base automatski dobiva:
#      - __tablename__ → ime tablice
#      - metadata      → kolekcija svih tablica (koristi Alembic)
#      - registry      → mapiranje Python klasa na tablice
#
#    Primjer (dolazi u sljedećem commitu):
#      class Club(Base):
#          __tablename__ = "clubs"
#          id: Mapped[int] = mapped_column(primary_key=True)
class Base(DeclarativeBase):
    pass

