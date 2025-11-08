from rest.models import Incident, IncidentCreate, IncidentUpdate, IncidentListQuery, IncidentListResponse
from sqlmodel import Session, func, select
from werkzeug.exceptions import NotFound
from datetime import datetime, UTC


def create_incident(session: Session, incident: IncidentCreate) -> Incident:
    """
    Создать новый инцидент
    """
    incident = Incident(description=incident.description, source=incident.source, status=incident.status)
    session.add(incident)
    session.commit()
    session.refresh(incident)
    return incident


def incident_get_by_id(session: Session, incident_id: int) -> Incident:
    """
    Получить инцидент по id
    """
    incident = session.get(Incident, incident_id)
    if not incident:
        raise NotFound(description=f"Incident with id {incident_id} not found")
    return incident


def incident_update_by_id(session: Session, incident_id: int, new_data: IncidentUpdate) -> Incident:
    """
    Обновить инцидент по id
    """
    incident = session.get(Incident, incident_id)
    if not incident:
        raise NotFound(description=f"Incident with id {incident_id} not found")
    is_updated = False
    if new_data.description is not None and incident.description != new_data.description:
        incident.description = new_data.description
        is_updated = True
    if new_data.source is not None and incident.source != new_data.source:
        incident.source = new_data.source
        is_updated = True
    if new_data.status is not None and incident.status != new_data.status:
        incident.status = new_data.status
        is_updated = True
    if is_updated:
        incident.updated_at = datetime.now(UTC)
        session.commit()
        session.refresh(incident)
    return incident


def incident_list_get(session: Session, query: IncidentListQuery) -> IncidentListResponse:
    """
    Получить список инцидентов с пагинацией и фильтрацией по статусу
    """
    filters = []
    if query.status:
        filters.append(Incident.status == query.status)
    stmt = select(Incident).where(*filters)
    total = session.scalar(select(func.count()).select_from(stmt.subquery()))
    stmt = stmt.offset((query.page - 1) * query.limit).limit(query.limit).order_by(Incident.created_at.desc())
    pages = total // query.limit if total % query.limit == 0 else total // query.limit + 1
    incidents = session.exec(stmt).all()
    return IncidentListResponse(incidents=incidents, total=total, page=query.page, pages=pages, limit=query.limit)
