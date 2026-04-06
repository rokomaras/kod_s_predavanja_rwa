# =============================================================
# jwt.py — Kreiranje i dekodiranje JWT tokena
# =============================================================
# Access token: kratkotrajan (15 min), koristi se za autorizaciju.
# Refresh token: dugotrajan (7 dana), koristi se za dobivanje
#   novog access tokena bez ponovnog logina.
#
# Claims (payload):
#   sub      — user ID (string po JWT konvenciji)
#   role     — "admin" ili "club"
#   club_id  — ID kluba (None za admine)
#   type     — "access" ili "refresh"
#   exp      — istek tokena (automatski, iz timedelta)
#   iss      — issuer (tko je izdao token)
# =============================================================

from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt

from app.core.config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
ALGORITHM = "HS256"


def create_access_token(
    user_id: int, role: str, club_id: int | None = None
) -> str:
    """Kreiraj kratkotrajan access token (15 min)."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "role": role,
        "club_id": club_id,
        "type": "access",
        "iss": settings.JWT_ISSUER,
        "exp": now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def create_refresh_token(user_id: int) -> str:
    """Kreiraj dugotrajan refresh token (7 dana)."""
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "iss": settings.JWT_ISSUER,
        "exp": now + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """
    Dekodiraj i validiraj JWT token.

    Baca JWTError ako:
      - token je istekao (exp)
      - potpis ne odgovara (secret)
      - format nije valjan
    """
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[ALGORITHM],
            issuer=settings.JWT_ISSUER,
        )
    except JWTError as e:
        raise JWTError(str(e)) from e
