from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

students=[]

class Student(BaseModel):
    name: str
    email: str
    age: int
    Roll_number:str
    Department:str


@app.get("/")
def read_root():
    return {"Hello": "World"}

class StudentResponse(Student):
    id: int
   

@app.get("/")
def read_root():
    return {"Hello": "World"}

def create_student(student:Student)->StudentResponse:
    students.append(student)
    return student
    
def get_student_by_roll(roll):
    for student in students:
        if student.Roll_number==roll:
            return student

def read_student(roll:str)->StudentResponse:
    return get_student_by_roll(roll)


def update_student(roll:str,student:Student)->StudentResponse:
    return StudentResponse(roll=roll, **student.dict())

def delete_student(roll:str):
    return StudentResponse(roll=roll, **student.dict())

@app.get("/students")
def read_students():
    return students

@app.post("/students")
def create_student_api(student:Student):
    return create_student(student)

@app.get("/students/{roll}")
def read_student_api(roll:str):
    return read_student(roll)

@app.put("/students/{roll}")
def update_student_api(roll:str,student:Student):
    return update_student(roll,student)

@app.delete("/students/{roll}")
def delete_student_api(roll:str):
    return delete_student(roll)