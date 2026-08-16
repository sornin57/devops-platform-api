from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)
API_KEY_HEADERS = {"X-API-Key": "dev-secret-key"}
INVALID_API_KEY_HEADERS = {"X-API-Key": "wrong-key"}


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_services_returns_list():
    response = client.get("/api/services")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_service_by_id_returns_service():
    response = client.get("/api/services/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == "auth-api"


def test_get_unknown_service_returns_404():
    response = client.get("/api/services/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_create_service_returns_created_service():
    payload = {
        "name": "data-pipeline",
        "status": "deploying",
        "version": "0.1.0",
        "environment": "development",
    }

    response = client.post(
        "/api/services",
        json=payload,
        headers=API_KEY_HEADERS,
    )

    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]
    assert response.json()["status"] == payload["status"]
    assert response.json()["version"] == payload["version"]
    assert response.json()["environment"] == payload["environment"]


def test_update_service_returns_updated_service():
    payload = {
        "name": "auth-api",
        "status": "degraded",
        "version": "1.0.1",
        "environment": "production",
    }

    response = client.put(
        "/api/services/1",
        json=payload,
        headers=API_KEY_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["id"] == 1
    assert response.json()["name"] == payload["name"]
    assert response.json()["status"] == payload["status"]
    assert response.json()["version"] == payload["version"]
    assert response.json()["environment"] == payload["environment"]


def test_delete_service_returns_deleted_service():
    payload = {
        "name": "cache-api",
        "status": "running",
        "version": "0.1.0",
        "environment": "development",
    }

    create_response = client.post(
        "/api/services",
        json=payload,
        headers=API_KEY_HEADERS,
    )
    service_id = create_response.json()["id"]

    delete_response = client.delete(
        f"/api/services/{service_id}",
        headers=API_KEY_HEADERS,
    )

    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Service deleted"
    assert delete_response.json()["service"]["id"] == service_id


def test_update_unknown_service_returns_404():
    payload = {
        "name": "unknown-api",
        "status": "running",
        "version": "1.0.0",
        "environment": "development",
    }

    response = client.put(
        "/api/services/999",
        json=payload,
        headers=API_KEY_HEADERS,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_delete_unknown_service_returns_404():
    response = client.delete(
        "/api/services/999",
        headers=API_KEY_HEADERS,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_filter_services_by_status():
    payload = {
        "name": "search-api",
        "status": "running",
        "version": "0.1.0",
        "environment": "production",
    }

    client.post(
        "/api/services",
        json=payload,
        headers=API_KEY_HEADERS,
    )

    response = client.get("/api/services?status=running")

    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert all(service["status"] == "running" for service in response.json())


def test_filter_services_by_environment():
    response = client.get("/api/services?environment=production")

    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert all(
        service["environment"] == "production"
        for service in response.json()
    )


def test_filter_services_with_invalid_status_returns_422():
    response = client.get("/api/services?status=broken")

    assert response.status_code == 422


def test_info_returns_app_metadata():
    response = client.get("/api/info")

    assert response.status_code == 200
    assert response.json() == {
        "app_name": "DevOps Platform API",
        "environment": "development",
    }


def test_create_service_without_api_key_returns_403():
    payload = {
        "name": "secure-api",
        "status": "running",
        "version": "1.0.0",
        "environment": "development",
    }

    response = client.post("/api/services", json=payload)

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API key"


def test_create_service_with_invalid_api_key_returns_403():
    payload = {
        "name": "secure-api",
        "status": "running",
        "version": "1.0.0",
        "environment": "development",
    }

    response = client.post(
        "/api/services",
        json=payload,
        headers=INVALID_API_KEY_HEADERS,
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API key"


def test_update_service_without_api_key_returns_403():
    payload = {
        "name": "auth-api",
        "status": "running",
        "version": "1.0.0",
        "environment": "production",
    }

    response = client.put("/api/services/1", json=payload)

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API key"


def test_delete_service_without_api_key_returns_403():
    response = client.delete("/api/services/1")

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid API key"
