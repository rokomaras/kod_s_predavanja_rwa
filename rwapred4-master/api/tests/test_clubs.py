# =============================================================
# test_clubs.py — Testovi za autorizaciju i ownership na club endpointima
# =============================================================

from httpx import AsyncClient

from tests.conftest import auth_header


# ---- Role testovi ------------------------------------------------

async def test_club_user_cannot_create_club(client: AsyncClient, club_and_user):
    """Club korisnik ne smije kreirati novi klub (403)."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        "/clubs/",
        json={"name": "Novi", "city": "Zagreb", "password": "pass123"},
        headers=headers,
    )
    assert resp.status_code == 403


async def test_admin_can_create_club(client: AsyncClient, admin_user):
    """Admin kreira klub — vraća 201 i generirani username."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.post(
        "/clubs/",
        json={"name": "Novi Klub", "city": "Zagreb", "password": "pass123"},
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Novi Klub"
    assert data["username"] == "novi-klub"


async def test_club_user_cannot_update_club(client: AsyncClient, club_and_user):
    """Club korisnik ne smije PATCH-irati klub (admin-only, 403)."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.patch(
        f"/clubs/{club.id}",
        json={"city": "NoviGrad"},
        headers=headers,
    )
    assert resp.status_code == 403


async def test_club_user_cannot_reset_password(client: AsyncClient, club_and_user):
    """Club korisnik ne smije resetirati lozinku (admin-only, 403)."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/clubs/{club.id}/reset-password",
        json={"new_password": "hacked123"},
        headers=headers,
    )
    assert resp.status_code == 403


async def test_unauthenticated_cannot_access_clubs(client: AsyncClient):
    """Bez tokena GET /clubs vraća 401."""
    resp = await client.get("/clubs/")
    assert resp.status_code == 401


# ---- Ownership testovi -------------------------------------------

async def test_club_sees_only_own_club_in_list(
    client: AsyncClient, club_and_user, club_b_and_user,
):
    """Club korisnik u listi vidi samo svoj klub."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.get("/clubs/", headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["name"] == "TestClub"


async def test_admin_sees_all_clubs_in_list(
    client: AsyncClient, admin_user, club_and_user, club_b_and_user,
):
    """Admin vidi sve klubove u listi."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.get("/clubs/", headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2


async def test_club_can_see_own_details(client: AsyncClient, club_and_user):
    """Club korisnik može vidjeti detalje svog kluba."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.get(f"/clubs/{club.id}", headers=headers)

    assert resp.status_code == 200
    assert resp.json()["name"] == "TestClub"


async def test_club_cannot_see_other_club_details(
    client: AsyncClient, club_and_user, club_b_and_user,
):
    """Club korisnik NE MOŽE vidjeti detalje drugog kluba (403)."""
    club_b, _ = club_b_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.get(f"/clubs/{club_b.id}", headers=headers)

    assert resp.status_code == 403
    assert resp.json()["code"] == "forbidden"


async def test_admin_can_see_any_club_details(
    client: AsyncClient, admin_user, club_and_user,
):
    """Admin može vidjeti detalje bilo kojeg kluba."""
    club, _ = club_and_user
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.get(f"/clubs/{club.id}", headers=headers)

    assert resp.status_code == 200


# ---- Admin CRUD testovi ------------------------------------------

async def test_admin_update_club(client: AsyncClient, admin_user, club_and_user):
    """Admin može ažurirati podatke kluba."""
    club, _ = club_and_user
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.patch(
        f"/clubs/{club.id}",
        json={"city": "NoviGrad"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["city"] == "NoviGrad"


async def test_admin_reset_password(client: AsyncClient, admin_user, club_and_user):
    """Admin resetira lozinku — klub se može prijaviti s novom."""
    club, _ = club_and_user
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.post(
        f"/clubs/{club.id}/reset-password",
        json={"new_password": "novasifra123"},
        headers=headers,
    )
    assert resp.status_code == 204

    login_resp = await client.post(
        "/auth/login",
        json={"username": "testclub", "password": "novasifra123"},
    )
    assert login_resp.status_code == 200


async def test_create_duplicate_club(client: AsyncClient, admin_user, club_and_user):
    """Kreiranje kluba s postojećim imenom vraća 409."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.post(
        "/clubs/",
        json={"name": "TestClub", "city": "Zagreb", "password": "pass123"},
        headers=headers,
    )
    assert resp.status_code == 409
    assert resp.json()["code"] == "duplicate"


async def test_get_nonexistent_club(client: AsyncClient, admin_user):
    """Dohvat nepostojećeg kluba vraća 404."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.get("/clubs/9999", headers=headers)
    assert resp.status_code == 404
