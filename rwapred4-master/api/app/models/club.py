# =============================================================
# club.py — Club ORM model
# =============================================================
# Predstavlja powerlifting klub u sustavu.
#
# Relacije:
#   Club 1 → 1 User   (jedan klub ima jednog login korisnika)
#   Club 1 → N Lifter  (dolazi u predavanju 5)
#
# Ključni constrainti:
#   - name je UNIQUE: ne smiju postojati dva kluba s istim imenom
#   - city je NOT NULL: svaki klub mora imati grad
# =============================================================

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class Club(Base):
    """
    Powerlifting klub.

    Atributi:
        id:             Surrogate primary key (autoincrement).
        name:           Službeni naziv kluba (jedinstven u sustavu).
        city:           Grad u kojem je klub registriran.
        contact_email:  Email za kontakt (opcionalan).
        contact_phone:  Telefon za kontakt (opcionalan).

    Relacije:
        users: Lista korisnika koji pripadaju ovom klubu.
               back_populates="club" znači da User.club pokazuje natrag.
    """

    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    users: Mapped[list[User]] = relationship(back_populates="club")

