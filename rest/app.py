from flask import current_app, make_response

from pydantic import BaseModel, ValidationError
from werkzeug.wrappers.response import Response
from flask_openapi3.models.info import Info
from flask_openapi3.openapi import OpenAPI
from rest.models import InternalServerError, NotFound
from rest.extensions import update_app_config, init_db, engine


info = Info(title="Incidents APP", version="1.0.0")


def register_api_views(app: OpenAPI) -> None:
    from rest.api import incidents
    
    app.register_api_view(incidents.api_view)


class ValidationErrorModel(BaseModel):
    code: str
    message: str


def validation_error_callback(e: ValidationError) -> Response:
    validation_error_object = ValidationErrorModel(code="400", message=e.json())
    response = make_response(validation_error_object.model_dump_json())
    response.headers["Content-Type"] = "application/json"
    response.status_code = getattr(current_app, "validation_error_status", 400)
    return response


def create_app() -> OpenAPI:
    app = OpenAPI(
        __name__,
        info=info,
        responses={404: NotFound, 500: InternalServerError},
        validation_error_status=400,
        validation_error_model=ValidationErrorModel,
        validation_error_callback=validation_error_callback
    )
    update_app_config(app)
    register_api_views(app)
    register_commands(app)
    register_errorhandlers(app)
    init_db(engine=engine)
    return app

def register_commands(app: OpenAPI) -> None:
    from rest.commands import drop_db
    
    app.cli.add_command(drop_db)


def register_errorhandlers(app: OpenAPI) -> None:
    """Регистрирует обработчики ошибок."""
    from werkzeug.exceptions import HTTPException
    from flask import jsonify, Response, request

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException) -> Response:
        """Обрабатывает все HTTP исключения и возвращает JSON вместо HTML."""
        response = jsonify({
            "code": e.code,
            # "name": e.name,
            "message": e.description
        })
        response.status_code = e.code or 500
        return response