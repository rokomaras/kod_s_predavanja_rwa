# =============================================================
# health.py — Health check endpoint (izdvojen iz main.py)
# =============================================================
# APIRouter je "mini-aplikacija" koju uključujemo u glavnu app.
# Prednost nad stavljanjem svega u main.py:
#   - Svaki modul (health, auth, lifters...) ima svoj router
#   - main.py ostaje čist — samo uključuje routere
#   - Lakše testiranje pojedinog modula
# =============================================================

from fastapi import APIRouter

# Kreiramo router instancu — ekvivalent Flask Blueprintu.
# Endpointi definirani ovdje nemaju prefix — prefix se dodaje
# u main.py kad pozovemo app.include_router(router, prefix="/health").
router = APIRouter()


@router.get("/")
def health():
    """
    Health check — potvrđuje da API radi.

    Vraća: {"status": "ok"}

    Ovaj endpoint pozivaju:
      - Deployment platforma (Railway) za liveness probe
      - Frontend pri inicijalizaciji (provjera je li backend dostupan)
      - Mi ručno za brzu provjeru nakon deploya
    """
    return {"status": "ok"}
