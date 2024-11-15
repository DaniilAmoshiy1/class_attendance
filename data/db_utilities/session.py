from data.config import DB_CONNECTION_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class StudentSession:
    engine = create_engine(DB_CONNECTION_URL)

    @classmethod
    def get_session(cls):
        session_class = sessionmaker(bind=cls.engine)
        session = session_class()
        return session
