from datetime import date, timedelta

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')


class Structure_table(BaseModel):
    name: str
    date: date
    status: str


students = [
    Structure_table(name='Даниил', date=date.today(), status='none'),
    Structure_table(name='Гоша', date=date.today(), status='none'),
    Structure_table(name='Геворг', date=date.today(), status='none'),
    Structure_table(name='Алексей', date=date.today(), status='none'),
    Structure_table(name='Дмитрий', date=date.today(), status='none'),
]


@app.get('/')
def get_table(request: Request):
    today = date.today()
    next_saturday = today + timedelta(days=(5 - today.weekday()) % 7)
    dates = [next_saturday + timedelta(days=i * 7) for i in range(6)]

    return templates.TemplateResponse(
        'pages/main_table.html',
        {
            'request': request,
            'students': students,
            'dates': dates
        }
    )


@app.get('/full_list_of_students')
def get_students(request: Request):
    unique_students = []
    seen_names = set()
    for student in students:
        if student.name not in seen_names:
            unique_students.append(student)
            seen_names.add(student.name)

    return templates.TemplateResponse(
        'pages/full_list_of_students.html',
        {
            'request': request,
            'students': unique_students
        }
    )


@app.get('/add_new_student')
def add_student_page(request: Request):
    return templates.TemplateResponse(
        'pages/add_new_student.html',
        {
            'request': request
        }
    )


@app.post('/add_new_student')
def add_student(request: Request, name: str = Form(...), status: str = Form(...)):
    global students
    if not any(student.name == name for student in students):
        new_student = Structure_table(name=name, date=date.today(), status=status)
        students.append(new_student)

    return templates.TemplateResponse(
        'pages/main_table.html',
        {
            'request': request,
            'students': students,
            'dates': [date.today() + timedelta(days=i * 7) for i in range(6)]
        }
    )
