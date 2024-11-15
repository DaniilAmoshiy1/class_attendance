from data.datamodel.students import Students
from data.data_generation import primary_example_student_names
from data.db_utilities.session import StudentSession


def prefill_students():
    with StudentSession.get_session() as session:
        students_name = [
            Students(name=name) for name in primary_example_student_names
        ]
        try:
            session.add_all(students_name)
            session.commit()
        except ValueError as err:
            raise err


if __name__ == '__main__':
    prefill_students()
