from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .model_base import SqlAlchemyBase


class StudentStatus(SqlAlchemyBase):
    __tablename__ = 'student_status'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey('students.id'), nullable=False)
    date_id: Mapped[int] = mapped_column(ForeignKey('dates.id'), nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    print('StudentStatus table has been up')
