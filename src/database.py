import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_timeout=5,
    connect_args={"connect_timeout": 5},
    echo=True,
)


SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
