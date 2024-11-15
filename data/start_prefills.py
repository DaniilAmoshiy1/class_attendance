from data.db_utilities.setup import reset_db, setup_db
from data.prefills import prefill_students, prefill_dates, prefill_statuses



def launch_prefills():
    reset_db()
    setup_db()

    prefill_dates.prefill_dates()
    prefill_students.prefill_students()
    prefill_statuses.prefill_statuses()


launch_prefills()
