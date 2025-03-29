from fastapi import APIRouter
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker

router = APIRouter()
engine = create_engine(
    URL.create(
        drivername='postgresql',
        username='postgres',
        password='postgres',
        host='postgres',
        port='5432',
        database='messenger',
    )
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
