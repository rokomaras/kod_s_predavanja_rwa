# =============================================================
# registration.py — Pydantic scheme za Registration entitet
# =============================================================

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

MALE_CATEGORIES = ["59", "66", "74", "83", "93", "105", "120", "120+"]
FEMALE_CATEGORIES = ["47", "52", "57", "63", "69", "76", "84", "84+"]
ALL_CATEGORIES = MALE_CATEGORIES + FEMALE_CATEGORIES


class RegistrationCreate(BaseModel):
    """POST /competitions/{comp_id}/registrations"""
    lifter_id: int
    category: str
    total: int = Field(ge=0, description="Najbolji total u zadnjih 12 mj. (0 = prvo natjecanje)")

    @field_validator("category")
    @classmethod
    def valid_category(cls, v: str) -> str:
        if v not in ALL_CATEGORIES:
            raise ValueError(
                f"Nepoznata kategorija: {v}. "
                f"Muške: {MALE_CATEGORIES}, Ženske: {FEMALE_CATEGORIES}"
            )
        return v


class RegistrationUpdate(BaseModel):
    """PATCH /competitions/{comp_id}/registrations/{id} — promjena kategorije/totala."""
    category: str | None = None
    total: int | None = Field(default=None, ge=0)

    @field_validator("category")
    @classmethod
    def valid_category(cls, v: str | None) -> str | None:
        if v is not None and v not in ALL_CATEGORIES:
            raise ValueError(
                f"Nepoznata kategorija: {v}. "
                f"Muške: {MALE_CATEGORIES}, Ženske: {FEMALE_CATEGORIES}"
            )
        return v


class RegistrationResponse(BaseModel):
    """Odgovor s podacima o prijavi."""
    id: int
    lifter_id: int
    competition_id: int
    category: str
    total: int
    status: str
    registered_at: datetime | None = None

    model_config = {"from_attributes": True}
