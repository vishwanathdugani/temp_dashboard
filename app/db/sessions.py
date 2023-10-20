from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

# Create the database engine
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

# Create a local session factory bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    FastAPI dependency to get a database session.
    Yields a new database session which is closed after use.

    Yields:
        Session: New database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
