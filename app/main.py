from fastapi import Depends, FastAPI, Header, HTTPException
from app.config import settings
from app.schemas import (
    Service,
    ServiceCreate,
    ServiceEnvironment,
    ServiceStatus,
)


app = FastAPI(title=settings.app_name)


services: list[Service] = [
    Service(
        id=1,
        name="auth-api",
        status="running",
        version="1.0.0",
        environment="production",
    ),
    Service(
        id=2,
        name="ml-worker",
        status="degraded",
        version="0.2.1",
        environment="staging",
    ),
]


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=403, detail="Invalid API key")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/info")
def get_info():
    return {
        "app_name": settings.app_name,
        "environment": settings.app_env,
    }


@app.get("/api/services", response_model=list[Service])
def get_services(
    status: ServiceStatus | None = None,
    environment: ServiceEnvironment | None = None,
):
    filtered_services = services

    if status is not None:
        filtered_services = [
            service for service in filtered_services if service.status == status
        ]

    if environment is not None:
        filtered_services = [
            service
            for service in filtered_services
            if service.environment == environment
        ]

    return filtered_services


@app.get("/api/services/{service_id}", response_model=Service)
def get_service(service_id: int):
    for service in services:
        if service.id == service_id:
            return service

    raise HTTPException(status_code=404, detail="Service not found")


@app.post("/api/services", response_model=Service, status_code=201)
def create_service(
    service_data: ServiceCreate,
    _: None = Depends(verify_api_key),
):
    new_service = Service(
        id=len(services) + 1,
        name=service_data.name,
        status=service_data.status,
        version=service_data.version,
        environment=service_data.environment,
    )

    services.append(new_service)
    return new_service


@app.put("/api/services/{service_id}", response_model=Service)
def update_service(
    service_id: int,
    service_data: ServiceCreate,
    _: None = Depends(verify_api_key),
):
    for index, service in enumerate(services):
        if service.id == service_id:
            updated_service = Service(
                id=service_id,
                name=service_data.name,
                status=service_data.status,
                version=service_data.version,
                environment=service_data.environment,
            )

            services[index] = updated_service
            return updated_service

    raise HTTPException(status_code=404, detail="Service not found")


@app.delete("/api/services/{service_id}")
def delete_service(
    service_id: int,
    _: None = Depends(verify_api_key),
):
    for index, service in enumerate(services):
        if service.id == service_id:
            deleted_service = services.pop(index)
            return {
                "message": "Service deleted",
                "service": deleted_service,
            }

    raise HTTPException(status_code=404, detail="Service not found")
