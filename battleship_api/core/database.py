from pydantic import AnyUrl
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


BaseModel = declarative_base()


def init(db_url: AnyUrl | None = None, **connect_args):
    """
    Initialize database connection engine instance and local Session class.
    After that creates all needed, non existing tables in connected database.

    Connection is initializing with database url given via `db_url`
    parameter or application setting. If it is not possible, use local sqlite
    file in app directory.

    Params:
        - [Optional] `db_url` - Database connection url.
            - Default: Local sqlite database connection url.
    """
    global engine
    global LocalSession

    engine = create_engine(
        db_url := db_url or "sqlite:///./db.sqlite3",
        connect_args={**connect_args})
    LocalSession = sessionmaker(engine, autoflush=False, autocommit=False)
    BaseModel.metadata.create_all(bind=engine)


def get_engine():
    """
    Returns database connection engine instance.
    """
    global engine
    return engine


def get_db_session():
    """
    Generator that at first yields the database session instance and nextly
    closes this session.
    Designed to be used as dependable function with FastAPI path operation
    functions.
    """
    global LocalSession
    db_session = LocalSession()
    try:
        yield db_session
    finally:
        db_session.close()
