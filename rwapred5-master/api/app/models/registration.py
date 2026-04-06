# =============================================================
# registration.py — Registration ORM model
# =============================================================
# Prijava natjecatelja na natjecanje. Povezuje Lifter i Competition
# s dodatnim podacima (kategorija, status, datum prijave).
#
# UniqueConstraint sprječava duplu prijavu istog liftera
# na isto natjecanje — baza je autoritet za integritet.
#
# Status:
#   "active"    — aktivna prijava
#   "withdrawn" — natjecatelj se odjavio (soft delete)
# =============================================================

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.competition import Competition
    from app.models.lifter import Lifter


class Registration(Base):
    __tablename__ = "registrations"
    __table_args__ = (
        UniqueConstraint("lifter_id", "competition_id",
                         name="uq_lifter_competition"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    lifter_id: Mapped[int] = mapped_column(
        ForeignKey("lifters.id"), nullable=False
    )
    competition_id: Mapped[int] = mapped_column(
        ForeignKey("competitions.id"), nullable=False
    )
    category: Mapped[str] = mapped_column(String(20), nullable=False)
    total: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(20), default="active")
    registered_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    lifter: Mapped[Lifter] = relationship(back_populates="registrations")
    competition: Mapped[Competition] = relationship(back_populates="registrations")
