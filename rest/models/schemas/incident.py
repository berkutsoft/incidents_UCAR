from datetime import datetime
from rest.models import Source, IncidentStatus
from sqlmodel import Field, SQLModel


class IncidentCreate(SQLModel):
    description: str = Field(..., description="Description")
    source: Source = Field(..., description="Source")
    status: IncidentStatus | None = Field(default=IncidentStatus.NEW, description="Status")


class IncidentUpdate(SQLModel):
    description: str | None = Field(default=None, description="Description")
    source: Source | None = Field(default=None, description="Source")
    status: IncidentStatus | None = Field(default=None, description="Status")


class IncidentResponse(SQLModel):
    id: int = Field(..., description="ID")
    description: str = Field(..., description="Description")
    source: Source = Field(..., description="Source")
    status: IncidentStatus = Field(..., description="Status")
    created_at: datetime = Field(..., description="Created at")
    updated_at: datetime = Field(..., description="Updated at")


class IncidentPath(SQLModel):
    id: int = Field(..., description="Incident ID")


class IncidentListQuery(SQLModel):
    page: int = Field(default=1, description="Page")
    limit: int = Field(default=10, description="Limit")
    status: IncidentStatus | None = Field(default=None, description="Status")



class IncidentListResponse(SQLModel):
    incidents: list[IncidentResponse] = Field(..., description="Incidents")
    total: int = Field(..., description="Total")
    page: int = Field(default=1, description="Page")
    pages: int = Field(..., description="Pages")
    limit: int = Field(default=10, description="Limit")