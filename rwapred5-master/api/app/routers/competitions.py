# =============================================================
# competitions.py — Competition endpointi
# =============================================================
# Admin: create, update
# Authenticated (admin + club): list, get
# =============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_user, get_db, require_role
from app.models.user import User
from app.schemas.competition import (
    CompetitionCreate,
    CompetitionResponse,
    CompetitionUpdate,
)
from app.services import competition_service

router = APIRouter()


@router.get("/", response_model=list[CompetitionResponse])
async def list_competitions(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Lista svih natjecanja (svi autenticirani korisnici)."""
    return await competition_service.list_competitions(db)


@router.post("/", response_model=CompetitionResponse, status_code=201)
async def create_competition(
    body: CompetitionCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    """Admin kreira natjecanje."""
    return await competition_service.create_competition(db, body)


@router.get("/{comp_id}", response_model=CompetitionResponse)
async def get_competition(
    comp_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Detalji natjecanja (svi autenticirani korisnici)."""
    return await competition_service.get_competition(db, comp_id)


@router.patch("/{comp_id}", response_model=CompetitionResponse)
async def update_competition(
    comp_id: int,
    body: CompetitionUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(require_role("admin")),
):
    """Admin ažurira natjecanje."""
    return await competition_service.update_competition(db, comp_id, body)
