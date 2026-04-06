# =============================================================
# lifter.py — Pydantic scheme za Lifter entitet
# =============================================================

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, field_validator


class LifterCreate(BaseModel):
    """POST /clubs/{club_id}/lifters"""
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    birth_date: date
    gender: Literal["M", "F"]

    @field_validator("birth_date")
    @classmethod
    def must_be_past(cls, v: date) -> date:
        if v >= date.today():
            raise ValueError("Datum rođenja mora biti u prošlosti")
        return v


class LifterUpdate(BaseModel):
    """PATCH /clubs/{club_id}/lifters/{id}"""
    first_name: str | None = Field(default=None, min_length=1, max_length=80)
    last_name: str | None = Field(default=None, min_length=1, max_length=80)
    birth_date: date | None = None
    gender: str | None = Field(default=None, pattern=r"^[MF]$")


class LifterResponse(BaseModel):
    """Odgovor s podacima o natjecatelju."""
    id: int
    first_name: str
    last_name: str
    birth_date: date
    gender: str
    club_id: int

    model_config = {"from_attributes": True}
