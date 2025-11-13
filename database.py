from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session
from typing import Generator
from decouple import config # Used to read the .env file

# 1. Database Configuration (Read from .env file)
# The config() function will safely retrieve the DATABASE_URL
SQLALCHEMY_DATABASE_URL = config("DATABASE_URL")

# 2. Create the SQLAlchemy Engine
# pool_pre_ping=True helps prevent connection problems after idle periods
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True
)

# 3. SessionLocal for creating individual sessions
# autocommit=False and autoflush=False allow for transactional behavior
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Base Class for Declarative Models
class Base(DeclarativeBase):
    """Base class which provides automated table name."""
    pass

# 5. Dependency Function for FastAPI
def get_db() -> Generator[Session, None, None]:
    """Provides a fresh database session for each request,
    ensuring it is closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
