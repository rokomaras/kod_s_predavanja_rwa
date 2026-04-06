# =============================================================
# test_auth.py — Testovi za autentikacijske endpointe
# =============================================================

from datetime import timedelta

from freezegun import freeze_time
from httpx import AsyncClient

from tests.conftest import auth_header


# ---- Login testovi ------------------------------------------------

async def test_login_ok(client: AsyncClient, admin_user):
    """Ispravan login vraća 200 i oba tokena."""
    resp = await client.post(
        "/auth/login",
        json={"username": "testadmin", "password": "admin123"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_wrong_password(client: AsyncClient, admin_user):
    """Krivi password vraća 401."""
    resp = await client.post(
        "/auth/login",
        json={"username": "testadmin", "password": "wrong"},
    )
    assert resp.status_code == 401
    assert resp.json()["code"] == "invalid_credentials"


async def test_login_nonexistent_user(client: AsyncClient):
    """Nepostojeći username vraća 401 (isti error kao krivi password)."""
    resp = await client.post(
        "/auth/login",
        json={"username": "ghost", "password": "whatever"},
    )
    assert resp.status_code == 401
    assert resp.json()["code"] == "invalid_credentials"


async def test_login_inactive_user(client: AsyncClient, inactive_user):
    """Deaktivirani korisnik ne može se prijaviti."""
    resp = await client.post(
        "/auth/login",
        json={"username": "inactive", "password": "pass123"},
    )
    assert resp.status_code == 401
    assert resp.json()["code"] == "invalid_credentials"


# ---- Refresh testovi ----------------------------------------------

async def test_refresh_ok(client: AsyncClient, admin_user):
    """Valjan refresh token izdaje novi par tokena."""
    login_resp = await client.post(
        "/auth/login",
        json={"username": "testadmin", "password": "admin123"},
    )
    refresh_token = login_resp.json()["refresh_token"]

    resp = await client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


async def test_refresh_with_access_token(client: AsyncClient, admin_user):
    """Access token se ne može koristiti za refresh."""
    login_resp = await client.post(
        "/auth/login",
        json={"username": "testadmin", "password": "admin123"},
    )
    access_token = login_resp.json()["access_token"]

    resp = await client.post(
        "/auth/refresh",
        json={"refresh_token": access_token},
    )
    assert resp.status_code == 401


async def test_refresh_expired(client: AsyncClient, admin_user):
    """Istekli refresh token (8 dana) vraća 401."""
    login_resp = await client.post(
        "/auth/login",
        json={"username": "testadmin", "password": "admin123"},
    )
    refresh_token = login_resp.json()["refresh_token"]

    with freeze_time(timedelta(days=8)):
        resp = await client.post(
            "/auth/refresh",
            json={"refresh_token": refresh_token},
        )
    assert resp.status_code == 401


# ---- /auth/me testovi ---------------------------------------------

async def test_me_ok(client: AsyncClient, admin_user):
    """Autenticirani korisnik dobiva svoje podatke."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.get("/auth/me", headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "testadmin"
    assert data["role"] == "admin"
    assert data["is_active"] is True
    assert data["club_id"] is None


async def test_me_no_token(client: AsyncClient):
    """Bez tokena GET /auth/me vraća 401."""
    resp = await client.get("/auth/me")
    assert resp.status_code == 401


async def test_me_expired_token(client: AsyncClient, admin_user):
    """Istekli access token (16 min) vraća 401."""
    headers = await auth_header(client, "testadmin", "admin123")

    with freeze_time(timedelta(minutes=16)):
        resp = await client.get("/auth/me", headers=headers)
    assert resp.status_code == 401
