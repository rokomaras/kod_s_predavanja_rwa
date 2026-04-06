# =============================================================
# registrations.py — Registration endpointi
#   (nested pod /competitions/{comp_id})
# =============================================================

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_db, require_role
from app.models.user import User
from app.schemas.registration import (
    RegistrationCreate,
    RegistrationResponse,
    RegistrationUpdate,
)
from app.services import registration_service

router = APIRouter()


@router.get("/", response_model=list[RegistrationResponse])
async def list_registrations(
    comp_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "club")),
):
    """Lista prijava za natjecanje (admin: sve, club: samo svoje)."""
    return await registration_service.list_registrations(db, comp_id, user)


@router.post("/", response_model=RegistrationResponse, status_code=201)
async def create_registration(
    comp_id: int,
    body: RegistrationCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "club")),
):
    """Prijavi natjecatelja na natjecanje."""
    return await registration_service.create_registration(db, comp_id, body, user)


@router.get("/{reg_id}", response_model=RegistrationResponse)
async def get_registration(
    comp_id: int,
    reg_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "club")),
):
    """Detalji prijave."""
    return await registration_service.get_registration(db, comp_id, reg_id, user)


@router.patch("/{reg_id}", response_model=RegistrationResponse)
async def update_registration(
    comp_id: int,
    reg_id: int,
    body: RegistrationUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "club")),
):
    """Promjena kategorije ili totala prijave."""
    return await registration_service.update_registration(
        db, comp_id, reg_id, body, user,
    )


@router.post("/{reg_id}/withdraw", response_model=RegistrationResponse)
async def withdraw_registration(
    comp_id: int,
    reg_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role("admin", "club")),
):
    """Odjava natjecatelja s natjecanja (soft delete)."""
    return await registration_service.withdraw_registration(
        db, comp_id, reg_id, user,
    )
