from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Date
from .model_base import SqlAlchemyBase



class Dates(SqlAlchemyBase):
    __tablename__ = 'dates'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    dates: Mapped[Date] = mapped_column(Date, nullable=False)
    print('Dates table has been up')
