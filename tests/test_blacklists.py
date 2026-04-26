import pytest

AUTH_HEADER = {"Authorization": "Bearer test-token-123"}
BAD_AUTH_HEADER = {"Authorization": "Bearer token-malo"}


# ─────────────────────────────────────────────
# POST /blacklists
# ─────────────────────────────────────────────

def test_create_blacklist_success(client):
    """Agrega un email exitosamente → 201"""
    response = client.post("/blacklists", json={
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "spam"
    }, headers=AUTH_HEADER)

    assert response.status_code == 201
    data = response.get_json()
    assert data["email"] == "test@example.com"
    assert data["app_uuid"] == "123e4567-e89b-12d3-a456-426614174000"
    assert data["blocked_reason"] == "spam"
    assert "ip_address" in data
    assert "created_at" in data


def test_create_blacklist_no_token(client):
    """Sin token → 401"""
    response = client.post("/blacklists", json={
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    })
    assert response.status_code == 401


def test_create_blacklist_bad_token(client):
    """Token inválido → 401"""
    response = client.post("/blacklists", json={
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    }, headers=BAD_AUTH_HEADER)
    assert response.status_code == 401


def test_create_blacklist_invalid_email(client):
    """Email mal formado → 400"""
    response = client.post("/blacklists", json={
        "email": "no-es-un-email",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    }, headers=AUTH_HEADER)
    assert response.status_code == 400


def test_create_blacklist_missing_app_uuid(client):
    """Falta app_uuid obligatorio → 400"""
    response = client.post("/blacklists", json={
        "email": "test@example.com",
    }, headers=AUTH_HEADER)
    assert response.status_code == 400


def test_create_blacklist_blocked_reason_too_long(client):
    """blocked_reason supera 255 caracteres → 400"""
    response = client.post("/blacklists", json={
        "email": "test@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "x" * 256,
    }, headers=AUTH_HEADER)
    assert response.status_code == 400


def test_create_blacklist_duplicate(client):
    """Mismo email + app_uuid dos veces → 409"""
    payload = {
        "email": "dup@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    }
    client.post("/blacklists", json=payload, headers=AUTH_HEADER)
    response = client.post("/blacklists", json=payload, headers=AUTH_HEADER)
    assert response.status_code == 409


def test_create_blacklist_without_blocked_reason(client):
    """blocked_reason es opcional → 201"""
    response = client.post("/blacklists", json={
        "email": "noreason@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
    }, headers=AUTH_HEADER)
    assert response.status_code == 201
    data = response.get_json()
    assert data["blocked_reason"] is None


# ─────────────────────────────────────────────
# GET /blacklists/<email>
# ─────────────────────────────────────────────

def test_check_blacklist_found(client):
    """Email que sí está en lista negra → is_blacklisted: true"""
    client.post("/blacklists", json={
        "email": "found@example.com",
        "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        "blocked_reason": "fraude",
    }, headers=AUTH_HEADER)

    response = client.get("/blacklists/found@example.com", headers=AUTH_HEADER)
    assert response.status_code == 200
    data = response.get_json()
    assert data["is_blacklisted"] is True
    assert data["blocked_reason"] == "fraude"


def test_check_blacklist_not_found(client):
    """Email que no está en lista negra → is_blacklisted: false"""
    response = client.get("/blacklists/nothere@example.com", headers=AUTH_HEADER)
    assert response.status_code == 200
    data = response.get_json()
    assert data["is_blacklisted"] is False
    assert data["blocked_reason"] is None


def test_check_blacklist_no_token(client):
    """Sin token → 401"""
    response = client.get("/blacklists/test@example.com")
    assert response.status_code == 401


def test_check_blacklist_bad_token(client):
    """Token inválido → 401"""
    response = client.get("/blacklists/test@example.com", headers=BAD_AUTH_HEADER)
    assert response.status_code == 401


def test_check_blacklist_invalid_email_format(client):
    """Email con formato inválido → 400"""
    response = client.get("/blacklists/no-es-un-email", headers=AUTH_HEADER)
    assert response.status_code == 400


# ─────────────────────────────────────────────
# GET /health
# ─────────────────────────────────────────────

def test_health_check(client):
    """Health endpoint responde 200"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"


def test_home_check(client):
    """Home endpoint responde 200"""
    response = client.get("/")
    assert response.status_code == 200


def test_falla_intencional(client):
    """Test intencional para demostrar pipeline fallido - REMOVER DESPUÉS"""
    response = client.get("/health")
    assert response.status_code == 999  # esto nunca va a ser 999