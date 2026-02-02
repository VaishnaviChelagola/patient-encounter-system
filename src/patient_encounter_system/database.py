from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "mysql+pymysql://mongouhd_evernorth:U*dgQkKRuEHe@cp-15.webhostbox.net:3306/mongouhd_evernorth"

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
