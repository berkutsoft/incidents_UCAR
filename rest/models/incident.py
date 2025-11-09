from datetime import UTC, datetime
from enum import Enum
from typing import ClassVar
from sqlmodel import Column, Field, SQLModel
from sqlalchemy.dialects import postgresql


class IncidentStatus(str, Enum):
    NEW = "new"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class Source(str, Enum):
    OPERATOR = "operator"
    MONITORING = "monitoring"
    PARTNER = "partner"
    SYSTEM = "system"


class Incident(SQLModel, table=True):
    __tablename__: ClassVar[str] = "incidents"
    
    id: int = Field(default=None, primary_key=True)
    description: str = Field(..., description="Description")
    created_at: datetime = Field(default_factory= lambda: datetime.now(UTC), description="Created at")
    updated_at: datetime = Field(default_factory= lambda: datetime.now(UTC), description="Updated at")
    status: IncidentStatus = Field(
        default=IncidentStatus.NEW,
        sa_column=Column(postgresql.ENUM(IncidentStatus), server_default=IncidentStatus.NEW.name, nullable=False, index=True),
        description="Status",
    )
    source: Source = Field(
        ...,
        sa_column=Column(postgresql.ENUM(Source), server_default=Source.OPERATOR.name, nullable=False, index=True),
        description="Source",
    )



    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} id={self.id}>"
