import click


@click.command(name='drop-db')
def drop_db() -> None:
    """
    Удаляет все таблицы в базе данных, создаёт новые и заполняет их начальными данными.
    """
    from rest.extensions.db import init_db, engine
    init_db(engine=engine, drop_tables=True)  # Инициализируем базу данных


@click.command(name='init-db')
@click.option('-d', '--drop-tables',
              help='Drop all tables in the database')
def init_db(drop_tables: bool = False) -> None:
    """
    Создаёт все таблицы в базе данных.
    """
    from rest.extensions.db import init_db, engine
    init_db(engine=engine, drop_tables=drop_tables)  # Инициализируем базу данных