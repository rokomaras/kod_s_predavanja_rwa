# =============================================================
# club.py — Pydantic scheme za Club entitet
# =============================================================
# Create/Update/Response pattern:
#   ClubCreate   — što admin šalje kad kreira klub
#   ClubUpdate   — parcijalni update (sva polja opcionalna)
#   ClubResponse — što API vraća (uključuje generirani username)
# =============================================================

from pydantic import BaseModel, Field


class ClubCreate(BaseModel):
    """POST /clubs — admin kreira klub s automatskim login korisnikom."""
    name: str = Field(min_length=1, max_length=120)
    city: str = Field(min_length=1, max_length=80)
    password: str = Field(min_length=6, max_length=128)
    contact_email: str | None = Field(default=None, max_length=255)
    contact_phone: str | None = Field(default=None, max_length=50)


class ClubUpdate(BaseModel):
    """PATCH /clubs/{id} — parcijalni update (samo poslana polja se mijenjaju)."""
    name: str | None = Field(default=None, min_length=1, max_length=120)
    city: str | None = Field(default=None, min_length=1, max_length=80)
    contact_email: str | None = None
    contact_phone: str | None = None


class ClubResponse(BaseModel):
    """Odgovor s podacima o klubu. Uključuje username login korisnika."""
    id: int
    name: str
    city: str
    contact_email: str | None = None
    contact_phone: str | None = None
    username: str | None = None

    model_config = {"from_attributes": True}


class ResetPasswordRequest(BaseModel):
    """POST /clubs/{id}/reset-password — admin postavlja novu lozinku."""
    new_password: str = Field(min_length=6, max_length=128)
