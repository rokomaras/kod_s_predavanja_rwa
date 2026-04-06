# =============================================================
# main.py — App factory i uključivanje routera
# =============================================================
# REFAKTORIRANO iz prethodnog commita!
#
# Prije: sve u ovoj datoteci (endpointi, konfiguracija, sve).
# Sada:  main.py samo SASTAVLJA aplikaciju od dijelova:
#   - config.py      → čita env varijable
#   - logging.py     → konfigurira logiranje
#   - errors.py      → registrira error handlere
#   - routers/*.py   → endpointi po modulima
#
# Što je app factory?
#   Funkcija create_app() koja KREIRA i KONFIGURIRA FastAPI instancu.
#   Prednosti:
#     1. Testovi mogu kreirati svježu app instancu za svaki test
#     2. Različite konfiguracije za dev/test/produkciju
#     3. Izbjegavamo "global state" probleme (moduli koji ovise o
#        redoslijedu importa)
#
# Pokretanje (nepromijenjeno):
#   uvicorn app.main:app --reload
#
# Uvicorn traži varijablu "app" u ovom modulu (zadnji red).
# =============================================================

import logging

from fastapi import FastAPI

from app.core.config import settings
from app.core.errors import AppError, app_error_handler
from app.core.logging import setup_logging
from app.routers.health import router as health_router

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """
    App factory — kreira, konfigurira i vraća FastAPI instancu.

    Redoslijed je bitan:
      1. Logging (da vidimo greške ako nešto pukne u koraku 2-4)
      2. FastAPI instanca s metapodacima
      3. Exception handleri (moraju biti registrirani prije routera)
      4. Routeri (endpointi)
    """
    # 1. Konfiguracija logiranja — mora biti prvo.
    setup_logging()

    # 2. Kreiranje FastAPI instance.
    #    docs_url: u dev okruženju Swagger je na /docs,
    #    u produkciji ga gasimo (ne želimo javno izloženu dokumentaciju).
    app = FastAPI(
        title="Powerlifting Registrations API",
        version="0.1.0",
        description="Sustav za prijavu natjecatelja na powerlifting natjecanja",
        docs_url="/docs" if settings.ENV == "dev" else None,
        redoc_url=None,
    )

    # 3. Registracija globalnog error handlera.
    #    Kad bilo koji endpoint baci AppError, FastAPI poziva
    #    app_error_handler umjesto defaultnog 500 odgovora.
    app.add_exception_handler(AppError, app_error_handler)

    # 4. Uključivanje routera.
    #    prefix="/health" znači: svi endpointi iz health routera
    #    dobivaju prefix, pa @router.get("/") postaje GET /health.
    app.include_router(health_router, prefix="/health", tags=["health"])

    logger.info("Aplikacija kreirana (env=%s)", settings.ENV)
    return app


# Uvicorn traži ovu varijablu: uvicorn app.main:app
# Poziva create_app() jednom pri startu servera.
app = create_app()
