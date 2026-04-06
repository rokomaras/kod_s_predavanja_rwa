# =============================================================
# lifter.py — Lifter ORM model
# =============================================================
# Natjecatelj koji pripada jednom klubu i može biti
# prijavljen na više natjecanja (kroz Registration).
#
# Relacije:
#   Club 1 → N Lifter
#   Lifter 1 → N Registration
# =============================================================

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.club import Club
    from app.models.registration import Registration


class Lifter(Base):
    __tablename__ = "lifters"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(80), nullable=False)
    last_name: Mapped[str] = mapped_column(String(80), nullable=False)
    birth_date: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)

    club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id"), nullable=False
    )

    club: Mapped[Club] = relationship(back_populates="lifters")
    registrations: Mapped[list[Registration]] = relationship(
        back_populates="lifter"
    )
