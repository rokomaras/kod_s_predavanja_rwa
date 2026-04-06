# =============================================================
# alembic/env.py — Okruženje za pokretanje migracija
# =============================================================
# Ova datoteka govori Alembicu KAKO se spojiti na bazu i
# ODAKLE čitati metadata (definicije tablica).
#
# Ključne prilagodbe u odnosu na default:
#   1. Koristimo ASYNC engine (asyncpg driver)
#   2. URL čitamo iz app.core.config.settings (ne iz alembic.ini)
#   3. target_metadata = Base.metadata (naši modeli)
#
# VAŽNO: import "from app.models import Base" MORA biti tu
# jer taj import pokreće registraciju svih modela u Base.metadata.
# Bez toga, autogenerate ne vidi nijednu tablicu!
# =============================================================

import asyncio
import sys
from logging.config import fileConfig
from pathlib import Path

# Dodajemo api/ direktorij na sys.path tako da Alembic može
# importirati "app" paket. Bez ovoga: ModuleNotFoundError.
# Path(__file__) → alembic/env.py → .parent.parent → api/
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from alembic import context  # noqa: E402
from sqlalchemy.ext.asyncio import create_async_engine  # noqa: E402

from app.core.config import settings  # noqa: E402
from app.models import Base  # noqa: E402, F401 — registrira sve modele

# Alembic Config objekt — daje pristup .ini vrijednostima.
config = context.config

# Postavljamo URL programski (umjesto iz .ini datoteke).
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Konfiguracija Python loggera iz .ini datoteke.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata koji Alembic koristi za autogenerate.
# Base.metadata sadrži definicije SVIH tablica (Club, User, ...).
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Pokreni migracije u "offline" modu — generira SQL bez spajanja na bazu.

    Korisno za:
      - Generiranje SQL skripti za DBA koji ih ručno izvršava
      - Okruženja gdje nema pristupa bazi iz CI/CD-a
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Pokreni migracije koristeći danu (sync) konekciju."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """
    Async wrapper — kreira async engine i pokreće migracije.

    Alembic sam po sebi nije async, ali mi koristimo async engine.
    Rješenje: connection.run_sync() "prebacuje" u sync kontekst
    unutar async konekcije.
    """
    connectable = create_async_engine(
        config.get_main_option("sqlalchemy.url"),
        pool_pre_ping=True,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """
    Pokreni migracije u "online" modu — spaja se na bazu i izvršava.

    Ovo je standardni mod koji koristimo u razvoju:
      alembic upgrade head
    """
    asyncio.run(run_async_migrations())


# Odabir moda: offline ako nema konekcije, inače online.
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

