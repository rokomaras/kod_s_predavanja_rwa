# =============================================================
# club.py — Club ORM model
# =============================================================
# Predstavlja powerlifting klub u sustavu.
#
# Relacije:
#   Club 1 → 1 User    (jedan klub ima jednog login korisnika)
#   Club 1 → N Lifter   (natjecatelji kluba)
# =============================================================

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.lifter import Lifter
    from app.models.user import User


class Club(Base):
    __tablename__ = "clubs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    contact_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    contact_phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    users: Mapped[list[User]] = relationship(back_populates="club")
    lifters: Mapped[list[Lifter]] = relationship(back_populates="club")

