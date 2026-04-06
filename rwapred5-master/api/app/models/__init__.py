# =============================================================
# models/__init__.py — Registar svih ORM modela
# =============================================================
# Ovdje importiramo Base i sve modele na jedno mjesto.
# Zašto?
#   1. Alembic čita Base.metadata da bi znao koje tablice postoje
#   2. Centralni import — umjesto:
#        from app.models.club import Club
#        from app.models.user import User
#      možemo pisati:
#        from app.models import Club, User
#   3. Osiguravamo da su svi modeli "registrirani" u Base.metadata
#      prije nego Alembic pokuša generirati migraciju
#
# VAŽNO: svaki novi model MORA biti importiran ovdje,
# inače ga Alembic neće vidjeti pri autogenerate!
# =============================================================

from app.core.database import Base
from app.models.club import Club
from app.models.competition import Competition
from app.models.lifter import Lifter
from app.models.registration import Registration
from app.models.user import User

__all__ = ["Base", "Club", "Competition", "Lifter", "Registration", "User"]
