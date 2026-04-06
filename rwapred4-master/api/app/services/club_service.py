# =============================================================
# club_service.py — Poslovna logika za upravljanje klubovima
# =============================================================

import re
import unicodedata

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.core.security import hash_password
from app.models.club import Club
from app.models.user import User
from app.repositories import club_repo, user_repo


def _slugify(text: str) -> str:
    """Pretvori ime kluba u username: 'PLK Behemot' → 'plk-behemot'."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    return re.sub(r"-+", "-", text).strip("-")


async def create_club(db: AsyncSession, name: str, city: str, password: str,
                      contact_email: str | None, contact_phone: str | None) -> tuple[Club, User]:
    """
    Kreira klub i automatski generira login korisnika.
    Vraća (club, user) tuple.
    """
    existing = await club_repo.get_by_name(db, name)
    if existing:
        raise AppError("duplicate", f"Klub '{name}' već postoji", 409)

    username = _slugify(name)
    existing_user = await user_repo.get_by_username(db, username)
    if existing_user:
        raise AppError("duplicate", f"Username '{username}' već postoji", 409)

    club = Club(
        name=name,
        city=city,
        contact_email=contact_email,
        contact_phone=contact_phone,
    )
    await club_repo.create(db, club)

    user = User(
        username=username,
        password_hash=hash_password(password),
        role="club",
        club_id=club.id,
    )
    db.add(user)
    await db.flush()

    return club, user


async def list_clubs(db: AsyncSession, current_user: User) -> list[Club]:
    """Admin vidi sve klubove, club korisnik vidi samo svoj."""
    if current_user.role == "admin":
        return await club_repo.get_all(db)
    club = await club_repo.get_by_id(db, current_user.club_id)
    return [club] if club else []


async def _get_or_404(db: AsyncSession, club_id: int) -> Club:
    """Interni helper: dohvati klub ili baci 404."""
    club = await club_repo.get_by_id(db, club_id)
    if not club:
        raise AppError("not_found", "Klub nije pronađen", 404)
    return club


async def get_club(db: AsyncSession, club_id: int, current_user: User) -> Club:
    """Dohvati klub po ID-u. Club korisnik smije vidjeti samo svoj klub."""
    club = await _get_or_404(db, club_id)
    if current_user.role == "club" and current_user.club_id != club_id:
        raise AppError("forbidden", "Ne možete pristupiti podacima drugog kluba", 403)
    return club


async def update_club(db: AsyncSession, club_id: int,
                      name: str | None, city: str | None,
                      contact_email: str | None, contact_phone: str | None) -> Club:
    """Admin ažurira podatke kluba (parcijalni update)."""
    club = await _get_or_404(db, club_id)

    if name is not None and name != club.name:
        existing = await club_repo.get_by_name(db, name)
        if existing:
            raise AppError("duplicate", f"Klub '{name}' već postoji", 409)
        club.name = name
    if city is not None:
        club.city = city
    if contact_email is not None:
        club.contact_email = contact_email
    if contact_phone is not None:
        club.contact_phone = contact_phone

    await db.flush()
    return club


async def reset_password(db: AsyncSession, club_id: int, new_password: str) -> None:
    """Admin postavlja novu lozinku za login korisnika kluba."""
    club = await _get_or_404(db, club_id)
    if not club.users:
        raise AppError("not_found", "Klub nema korisnika", 404)
    club.users[0].password_hash = hash_password(new_password)
    await db.flush()
