from flask_openapi3.models.tag import Tag
from flask_openapi3.view import APIView
from rest.helpers.db import get_session
from sqlmodel import Session
from rest.models import BadRequest, IncidentCreate, IncidentResponse, IncidentPath, IncidentUpdate, IncidentListQuery, IncidentListResponse
from http import HTTPStatus
from typing import Literal, Tuple
from werkzeug.wrappers.response import Response
from rest.crud import create_incident, incident_update_by_id, incident_get_by_id, incident_list_get


tag = Tag(name="Incidents", description="Incidents API")

api_view = APIView(url_prefix="/api/v1/incidents", view_tags=[tag], view_security=None)


@api_view.route("/")
class IncidentsAPI:

    @api_view.doc(summary="Получить список инцидентов", responses={200: IncidentListResponse, 400: BadRequest})
    @get_session
    def get(self, session: Session, query: IncidentListQuery) -> Tuple[Response, int]:
        incidents = incident_list_get(session=session, query=query)
        return incidents.model_dump_json(), HTTPStatus.OK.value
    
    @api_view.doc(summary="Создать инцидент", responses={201: IncidentResponse, 400: BadRequest})
    @get_session
    def post(self, session: Session, body: IncidentCreate) -> Tuple[Response, int]:
        incident = create_incident(session=session, incident=body)
        return incident.model_dump_json(), HTTPStatus.CREATED.value


@api_view.route("/<int:id>")
class IncidentAPI:
    
    @api_view.doc(summary="Получить инцидент по id", responses={200: IncidentResponse, 400: BadRequest})
    @get_session
    def get(self, session: Session, path: IncidentPath) -> Tuple[Response, int]:
        incident = incident_get_by_id(session=session, incident_id=path.id)
        return incident.model_dump_json(), HTTPStatus.OK.value

    @api_view.doc(summary="Обновить инцидент по id", responses={200: IncidentResponse, 400: BadRequest})
    @get_session
    def put(self, session: Session, path: IncidentPath, body: IncidentUpdate) -> Tuple[Response, int]:
        incident = incident_update_by_id(session=session, incident_id=path.id, new_data=body)
        return incident.model_dump_json(), HTTPStatus.OK.value