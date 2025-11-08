from config import Config
from flask_openapi3.openapi import OpenAPI

config: Config = Config("")


def update_app_config(app: OpenAPI) -> None:
    app.config.update(config)
    config.update(app.config)
    app.secret_key = config.SECRET_KEY
    return None
