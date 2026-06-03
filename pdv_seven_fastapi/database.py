from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from pdv_seven_fastapi.settings import Settings

engine = create_engine(Settings().DATABASE_URL, future=True)


def get_session():
    with Session(engine) as session:
        yield session
