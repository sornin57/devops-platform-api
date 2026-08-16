from typing import Literal

from pydantic import BaseModel, Field


ServiceStatus = Literal["running", "stopped", "degraded", "deploying"]
ServiceEnvironment = Literal["development", "staging", "production"]


class Service(BaseModel):
    id: int
    name: str
    status: ServiceStatus
    version: str
    environment: ServiceEnvironment


class ServiceCreate(BaseModel):
    name: str = Field(..., min_length=1)
    status: ServiceStatus
    version: str = Field(..., min_length=1)
    environment: ServiceEnvironment