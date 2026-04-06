# =============================================================
# user.py — User ORM model
# =============================================================
# Korisnik sustava — može biti admin ili club user.
#
# Role:
#   "admin" — upravlja natjecanjima, vidi sve klubove
#   "club"  — prijavljuje natjecatelje svog kluba
#
# Dizajnerske odluke:
#   - role je String (ne Enum) — jednostavnije za početak,
#     validacija se radi u Pydantic schema sloju
#   - club_id je nullable: admin NEMA klub (club_id = NULL)
#   - username je UNIQUE: sprječava duplicirane loginove
#     (za club usere auto-generiran iz naziva kluba)
#   - password_hash: NIKAD ne spremamo lozinku u čistom tekstu!
#   - is_active: omogućuje deaktivaciju korisnika bez brisanja
# =============================================================

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.club import Club


class User(Base):
    """
    Korisnik sustava (admin ili club user).

    Atributi:
        id:            Surrogate primary key.
        username:      Login korisničko ime (jedinstven u sustavu).
        password_hash: Bcrypt hash lozinke (NIKAD plain text).
        role:          "admin" ili "club".
        is_active:     Može li se korisnik prijaviti.
        club_id:       FK prema klubu (NULL za admine).

    Relacije:
        club: Klub kojem korisnik pripada (None za admine).
              back_populates="users" znači da Club.users pokazuje natrag.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)

    # Foreign key prema clubs tablici.
    # nullable=True jer admin korisnik ne pripada nijednom klubu.
    club_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("clubs.id"), nullable=True
    )

    # ORM relationship — omogućuje user.club umjesto ručnog querya.
    club: Mapped[Optional[Club]] = relationship(back_populates="users")

