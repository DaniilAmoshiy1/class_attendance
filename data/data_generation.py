from datetime import date, timedelta

students: list = []
dates: list[date] = []

primary_example_student_names: list[str] = [
    'Даниил',
    'Гоша',
    'Дмитрий',
    'Геворг',
    'Алексей',
]


def initialize_dates():
    today = date.today()
    next_saturday = today + timedelta(days=(5 - today.weekday()) % 7)
    end_of_year = date(today.year, 12, 31)

    current_date = next_saturday
    while current_date <= end_of_year:
        dates.append(current_date)
        current_date += timedelta(days=7)

    return dates
