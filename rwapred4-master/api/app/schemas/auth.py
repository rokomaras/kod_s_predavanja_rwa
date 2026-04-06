# =============================================================
# auth.py — Pydantic schemed za autentikaciju
# =============================================================

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    """Tijelo POST /auth/login requesta."""
    username: str = Field(min_length=1, max_length=50)
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    """Odgovor s JWT tokenima nakon uspješnog logina ili refresha."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    """Tijelo POST /auth/refresh requesta."""
    refresh_token: str


class UserResponse(BaseModel):
    """Prikaz trenutnog korisnika (GET /auth/me)."""
    id: int
    username: str
    role: str
    is_active: bool
    club_id: int | None = None

    model_config = {"from_attributes": True}
