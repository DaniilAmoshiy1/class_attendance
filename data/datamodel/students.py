from sqlalchemy.orm import Mapped, mapped_column
from .model_base import SqlAlchemyBase


class Students(SqlAlchemyBase):
    __tablename__ = 'students'

    id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    print('Students table has been up')
