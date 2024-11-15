from datetime import date
import runpy

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# In fact, initialization is used, don't delete this import.
from config import INITIALIZATION, REDIRECT_CODE
from data.datamodel.students import Students
from data.datamodel.dates import Dates
from data.datamodel.student_status import StudentStatus
from data.db_utilities.session import StudentSession


app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')



def get_data_from_db():
    global INITIALIZATION
    if not INITIALIZATION:
        runpy.run_path('data/start_prefills.py')
        INITIALIZATION = True

    with StudentSession.get_session() as session:
        students_db = session.query(Students).all()
        students = {student.id: student.name for student in students_db}

        dates_db = session.query(Dates).all()
        dates = {period.id: period.dates for period in dates_db}

        statuses = session.query(StudentStatus).all()
        status_dict = {}
        for status in statuses:
            if status.student_id not in status_dict:
                status_dict[status.student_id] = {}
            status_dict[status.student_id][status.date_id] = status.status


    return students, dates, status_dict


@app.get('/')
def get_table(request: Request):

    students, dates, status_dict = get_data_from_db()
    return templates.TemplateResponse(
        'main_table.html',
        {
            'request': request,
            'students': students,
            'dates': dates,
            'status_dict': status_dict
        }
    )


@app.get('/full_list_of_students')
def get_students(request: Request):
    students, _, _ = get_data_from_db()
    return templates.TemplateResponse(
        'pages/full_list_of_students.html',
        {
            'request': request,
            'students': students
        }
    )


@app.get('/add_new_student')
def get_add_student(request: Request):
    return templates.TemplateResponse(
        'pages/add_new_student.html',
        {
            'request': request
        }
    )


@app.post('/add_new_student')
def add_student(request: Request, name: str = Form()):
    with StudentSession.get_session() as session:
        if not session.query(Students).filter_by(name=name).first():
            new_student = Students(name=name)
            session.add(new_student)
            session.commit()

            dates = session.query(Dates).all()
            for date in dates:
                new_status = StudentStatus(student_id=new_student.id, date_id=date.id, status='none')
                session.add(new_status)

            session.commit()
            session.close()

    students, dates, status_dict = get_data_from_db()
    return templates.TemplateResponse(
        'main_table.html',
        {
            'request': request,
            'students': students,
            'dates': dates,
            'status_dict': status_dict
        }
    )


@app.get('/delete_student')
def get_delete_page(request: Request, error: str = None):
    students, _, _ = get_data_from_db()
    return templates.TemplateResponse(
        'pages/delete_student.html',
        {
            'request': request,
            'error': error,
            'students': students
        }
    )


@app.post('/delete_student')
def delete_student(request: Request, student_name: str = Form()):
    with StudentSession.get_session() as session:
        student = session.query(Students).filter_by(name=student_name).first()
        if student:
            session.query(StudentStatus).filter_by(student_id=student.id).delete()

            session.delete(student)
            session.commit()
            students, dates, status_dict = get_data_from_db()

            return templates.TemplateResponse(
                'main_table.html',
                {
                    'request': request,
                    'students': students,
                    'dates': dates,
                    'status_dict': status_dict
                }
            )
        else:
            return RedirectResponse(
                url=f'/delete_student?error=This name not in table',
                status_code=REDIRECT_CODE
            )


@app.get('/dates')
def get_dates(request: Request):
    _, dates, _ = get_data_from_db()
    return templates.TemplateResponse(
        'pages/dates.html',
        {
            'request': request,
            'dates': dates
        }
    )


@app.get('/add_date')
def get_add_date(request: Request, error: str = None):
    return templates.TemplateResponse(
        '/pages/add_date.html',
        {
            'request': request,
            'error': error
        }
    )


@app.post('/add_date')
def add_date(request: Request, new_date: str = Form()):
    try:
        new_date = date.fromisoformat(new_date)
    except ValueError:
        return RedirectResponse(
            url=f'/add_date?error=Invalid date format',
            status_code=REDIRECT_CODE
        )
    with StudentSession.get_session() as session:
        if not session.query(Dates).filter_by(dates=new_date).first():

            new_date_record = Dates(dates=new_date)
            session.add(new_date_record)
            session.commit()

            students = session.query(Students).all()

            for student in students:
                new_status = StudentStatus(student_id=student.id, date_id=new_date_record.id, status='none')
                session.add(new_status)

            session.commit()

            students, dates, status_dict = get_data_from_db()

    return templates.TemplateResponse(
        'main_table.html',
        {
            'request': request,
            'students': students,
            'dates': dates,
            'status_dict': status_dict
        }
    )


@app.get('/delete_date')
def get_delete_date(request: Request, error: str = None):
    _, dates, _ = get_data_from_db()
    return templates.TemplateResponse(
        'pages/delete_date.html', {
            'request': request,
            'error': error,
            'dates': dates
        }
    )


@app.post('/delete_date')
def delete_date(request: Request, delete_one_date: str = Form(...)):
    try:
        delete_date = date.fromisoformat(delete_one_date)
    except ValueError:
        return RedirectResponse(
            url=f'/add_date?error=Invalid date format',
            status_code=REDIRECT_CODE
        )
    with StudentSession.get_session() as session:
        date_record = session.query(Dates).filter_by(dates=delete_date).first()
        if date_record:
            session.query(StudentStatus).filter_by(date_id=date_record.id).delete()

            session.delete(date_record)
            session.commit()

            students, dates, status_dict = get_data_from_db()

            return templates.TemplateResponse(
                'main_table.html',
                {
                    'request': request,
                    'students': students,
                    'dates': dates,
                    'status_dict': status_dict
                }
            )
        else:
            return RedirectResponse(
                url=f'/delete_date?error=Date not found',
                status_code=REDIRECT_CODE
            )


@app.get('/update_student_status')
def get_update_student_status(request: Request, error: str = None):
    students, dates, _ = get_data_from_db()
    return templates.TemplateResponse(
        'pages/update_student_status.html',
        {
            'request': request,
            'students': students,
            'dates': dates,
            'error': error
        }
    )


@app.post('/update_student_status')
def update_student_status(request: Request, name: str = Form(), date_str: str = Form(), status: str = Form()):
    try:
        date_obj = date.fromisoformat(date_str)
    except ValueError:
        return RedirectResponse(
            url=f'/update_student_status?error=Invalid date format',
            status_code=REDIRECT_CODE
        )

    with (StudentSession.get_session() as session):
        student = session.query(Students).filter_by(name=name).first()
        date_record = session.query(Dates).filter_by(dates=date_obj).first()
        if student and date_record:
            status_record = session.query(StudentStatus).filter_by(
                student_id=student.id,
                date_id=date_record.id
            ).first()
            if status_record:
                status_record.status = status
            else:
                new_status_record = StudentStatus(student_id=student.id, date_id=date_record.id, status=status)
                session.add(new_status_record)
            session.commit()

    students, dates, status_dict = get_data_from_db()
    return templates.TemplateResponse(
        'main_table.html',
        {
            'request': request,
            'students': students,
            'dates': dates,
            'status_dict': status_dict
        }
    )

# This is function I couldn't do.
# @app.post('/reset_data')
# def reset_data():
#     # reset_db()
#     # setup_db()
#     os.remove(DB_PATH)
#     runpy.run_path('data/start_prefills.py')
#     return RedirectResponse(url='/', status_code=REDIRECT_CODE)
#
#
#
#
#     # global INITIALIZATION
#     # INITIALIZATION = False
#     #
#     # runpy.run_path('main.py')
#     #
#     # students, dates, status_dict = get_data_from_db()
#     # print('reset_data has been worked')
#     # return templates.TemplateResponse(
#     #     'main_table.html',
#     #     {
#     #         'request': request,
#     #         'students': students,
#     #         'dates': dates,
#     #         'status_dict': status_dict
#     #     }
#     # )


@app.post('/delete_values')
def delete_values():
    with StudentSession.get_session() as session:
        session.query(Students).delete()
        session.query(Dates).delete()
        session.query(StudentStatus).delete()
        session.commit()

    return RedirectResponse(url='/', status_code=REDIRECT_CODE)
