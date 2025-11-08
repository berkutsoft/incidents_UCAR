from sqlalchemy import Engine, inspect
from sqlmodel import SQLModel, Session, create_engine, select
from rest import crud
from rest.models import *  # Import models
from rest.extensions.settings import config
from sqlalchemy import text

engine: Engine = create_engine(config.SQLALCHEMY_DATABASE_URL)


def create_tables_db(engine: Engine) -> None:
    """
    Создаёт все таблицы в базе данных.
    """
    SQLModel.metadata.create_all(engine)


def fill_db(engine: Engine) -> None:
    """
    Заполняет базу данных начальными данными.
    """
    pass


def drop_db(engine: Engine) -> None:
    """
    Удаляет все таблицы в базе данных, включая таблицу alembic_version.
    """
    with Session(engine) as session:
        inspector = inspect(session.bind)
        if "alembic_version" in inspector.get_table_names():
            session.execute(text("TRUNCATE TABLE alembic_version"))
            session.commit()
    SQLModel.metadata.drop_all(engine)  # pragma: no cover


def init_db(*, engine: Engine, drop_tables: bool = False) -> None:
    """
    Инициализирует базу данных.
    Если drop_tables=True, удаляет все таблицы в базе данных перед созданием новых.
    """
    if drop_tables:
        drop_db(engine)  # удаляет все таблицы в базе данных    # pragma: no cover
    create_tables_db(engine)  # создаёт все таблицы в базе данных
    fill_db(engine)  # заполняет базу данных начальными данными
