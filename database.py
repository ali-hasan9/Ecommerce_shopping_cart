from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLite file will be created in project root
DATABASE_URL = "sqlite:///./ecommerce.db"
# connect_args needed only for SQLite (allows multi-thread access)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Each request gets its own session (database conversation)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class — all our models will inherit from this
Base = declarative_base()


def get_db():
    """
    Dependency that provides a DB session per request.
    Yields the session, then closes it when the request is done.
    This is how FastAPI manages DB connections safely.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()