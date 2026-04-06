# =============================================================
# competition.py — Competition ORM model
# =============================================================
# Natjecanje s dva roka:
#   prelim_deadline — do kad klubovi mogu slati prijave
#   final_deadline  — nakon čega su prijave zaključane
#
# Faze (implementiramo u P6):
#   OPEN           — datum < prelim_deadline
#   PRELIM_PASSED  — prelim_deadline <= datum < final_deadline
#   CLOSED         — datum >= final_deadline
# =============================================================

from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.registration import Registration


class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)

    prelim_deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    final_deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    registrations: Mapped[list[Registration]] = relationship(
        back_populates="competition"
    )
