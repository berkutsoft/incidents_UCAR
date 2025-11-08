import logging
import os
from flask.config import Config as FlaskConfig


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Config(FlaskConfig):
    logger = logging.getLogger(__name__)
    SECRET_KEY: str | None = os.environ.get("SECRET_KEY")
    HOST: str = os.environ.get("HOST", "0.0.0.0")
    PORT: int = int(os.environ.get("PORT", 8600))
    API_URL: str = os.environ.get("API_URL", f"http://{HOST}:{PORT}")
    ROOT_DIR: str = ROOT_DIR
    SQLALCHEMY_DATABASE_URL: str = (
        os.environ.get("SQLALCHEMY_DATABASE_URL")
        or f"postgresql+psycopg2://{os.environ.get('POSTGRES_USER', 'incidents_app')}:"
           f"{os.environ.get('POSTGRES_PASSWORD', 'incidents_app')}@"
           f"{os.environ.get('POSTGRES_HOST', 'localhost')}:{os.environ.get('POSTGRES_PORT', 5432)}/"
           f"{os.environ.get('POSTGRES_DB', 'incidents_app')}"
    )