from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict


app = FastAPI()


class StudentCreate(BaseModel):
    name: str
    age: int
    email: str
    roll_number: str
    department: str


class Student(StudentCreate):
    id: int


# In-memory store for demonstration purposes
_db: Dict[int, Student] = {}
_next_id = 1


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/student", response_model=Student)
def create_student(student: StudentCreate):
    global _next_id
    student_obj = Student(id=_next_id, **student.dict())
    _db[_next_id] = student_obj
    _next_id += 1
    return student_obj


@app.get("/student/{id}", response_model=Student)
def read_student(id: int):
    student = _db.get(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/student/{id}", response_model=Student)
def update_student(id: int, student: StudentCreate):
    existing = _db.get(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Student not found")
    updated = Student(id=id, **student.dict())
    _db[id] = updated
    return updated


@app.delete("/student/{id}")
def delete_student(id: int):
    if id not in _db:
        raise HTTPException(status_code=404, detail="Student not found")
    del _db[id]
    return {"detail": "deleted"}