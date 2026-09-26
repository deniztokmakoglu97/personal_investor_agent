from collections.abc import Iterator

from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from personal_investor_agent.settings import get_settings

settings = get_settings()

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.investor_db_user,
    password=settings.investor_db_password.get_secret_value(),
    host=settings.investor_db_host,
    port=settings.investor_db_port,
    database=settings.investor_db,
)

engine: Engine = create_engine(
    database_url,
    pool_pre_ping=True,
)


def get_database_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def check_database_connection() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
