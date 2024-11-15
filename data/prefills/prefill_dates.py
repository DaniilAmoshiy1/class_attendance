from data.datamodel.dates import Dates
from data.data_generation import initialize_dates
from data.db_utilities.session import StudentSession


def prefill_dates():
    with StudentSession.get_session() as session:
        dates_for_students = [
            Dates(dates=date) for date in initialize_dates()
        ]
        try:
            session.add_all(dates_for_students)
            session.commit()

        except ValueError as err:
            raise err


if __name__ == '__main__':
    prefill_dates()
