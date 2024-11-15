from data.datamodel.students import Students
from data.datamodel.dates import Dates
from data.datamodel.student_status import StudentStatus
from data.db_utilities.session import StudentSession


def prefill_statuses():
    with StudentSession.get_session() as session:
        students = session.query(Students).all()
        dates = session.query(Dates).all()

        statuses = []
        for student in students:
            for date in dates:
                statuses.append(StudentStatus(student_id=student.id, date_id=date.id, status='none'))
        try:
            session.add_all(statuses)
            session.commit()
        except ValueError as err:
            raise err


if __name__ == '__main__':
    prefill_statuses()
