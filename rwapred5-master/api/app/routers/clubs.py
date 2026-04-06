# =============================================================
# clubs.py — Club endpointi (admin upravljanje klubovima)
# =============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_role
from app.models.club import Club
from app.models.user import User
from app.schemas.club import ClubCreate, ClubResponse, ClubUpdate, ResetPasswordRequest
from app.services import club_service

router = APIRouter()


def _club_response(club: Club, username: str | None = None) -> ClubResponse:
    """Pretvori Club ORM objekt u ClubResponse, uključujući username."""
    uname = username or (club.users[0].username if club.users else None)
    return ClubResponse(
        id=club.id,
        name=club.name,
        city=club.city,
        contact_email=club.contact_email,
        contact_phone=club.contact_phone,
        username=uname,
    )


@router.post("/", response_model=ClubResponse, status_code=201)
async def create_club(
    body: ClubCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    """Admin kreira klub — automatski se kreira login korisnik."""
    club, user = await club_service.create_club(
        db, body.name, body.city, body.password,
        body.contact_email, body.contact_phone,
    )
    return _club_response(club, username=user.username)


@router.get("/", response_model=list[ClubResponse])
async def list_clubs(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "club")),
):
    """Admin vidi sve klubove, club korisnik vidi samo svoj."""
    clubs = await club_service.list_clubs(db, user)
    return [_club_response(c) for c in clubs]


@router.get("/{club_id}", response_model=ClubResponse)
async def get_club(
    club_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "club")),
):
    """Detalji kluba s ownership provjerom."""
    club = await club_service.get_club(db, club_id, user)
    return _club_response(club)


@router.patch("/{club_id}", response_model=ClubResponse)
async def update_club(
    club_id: int,
    body: ClubUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    """Admin ažurira podatke kluba."""
    club = await club_service.update_club(
        db, club_id, body.name, body.city,
        body.contact_email, body.contact_phone,
    )
    return _club_response(club)


@router.post("/{club_id}/reset-password", status_code=204)
async def reset_password(
    club_id: int,
    body: ResetPasswordRequest,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    """Admin resetira lozinku login korisnika kluba."""
    await club_service.reset_password(db, club_id, body.new_password)
