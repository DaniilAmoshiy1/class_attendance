from data.datamodel.model_base import SqlAlchemyBase
from data.db_utilities.session import StudentSession


def reset_db():
    SqlAlchemyBase.metadata.drop_all(StudentSession.engine)


def setup_db():
    SqlAlchemyBase.metadata.create_all(StudentSession.engine)
