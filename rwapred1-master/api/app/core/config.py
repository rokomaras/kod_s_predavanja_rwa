# =============================================================
# config.py — Centralna konfiguracija aplikacije
# =============================================================
# Svi env varovi se čitaju na JEDNOM mjestu, a ne razbacani
# po kodu sa os.getenv("..."). Prednosti:
#   1. Tipizirana konfiguracija (IDE autocompletion)
#   2. Validacija pri startu — ako fali DATABASE_URL, odmah pukne
#   3. Default vrijednosti za development
#
# Korištenje u ostatku koda:
#   from app.core.config import settings
#   print(settings.DATABASE_URL)
# =============================================================

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Pydantic BaseSettings automatski čita env varijable.
    Redoslijed prioriteta:
      1. Stvarne env varijable sustava (najviši prioritet)
      2. Vrijednosti iz .env datoteke
      3. Default vrijednosti definirane ovdje (najniži prioritet)
    """

    # Okruženje: "dev" uključuje debug logging i Swagger UI.
    # U produkciji postavimo na "production".
    ENV: str = "dev"

    # Connection string za bazu. Format:
    # postgresql+asyncpg://<user>:<pass>@<host>:<port>/<db_name>
    # "asyncpg" dio govori SQLAlchemyu koji driver da koristi.
    DATABASE_URL: str = "postgresql+asyncpg://pl_user:pl_pass@localhost:5432/pl_reg"

    # JWT (JSON Web Token) konfiguracija — koristi se od predavanja 3.
    # Secret MORA biti promijenjen u produkciji!
    JWT_SECRET: str = "change-me-in-production"
    JWT_ISSUER: str = "sit-unizd"

    # model_config govori Pydanticu ODAKLE čitati env varijable.
    # env_file=".env" znači: traži .env datoteku u working directoriju.
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


# Singleton instanca — importamo je svugdje u projektu.
# Kreira se jednom pri prvom importu ovog modula.
settings = Settings()
