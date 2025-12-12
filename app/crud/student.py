from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from models.student import Student
from models.enrolment import Enrolment
from schemas.student import StudentCreate, StudentUpdate
from datetime import date

import crud.enrolment as enrolment_crud

from fastapi.responses import HTMLResponse

#Create Student
async def create_student(db: AsyncSession, student_data: StudentCreate):
    try:
        # check for same emails
        result = await db.execute(
            select(Student).where(Student.email == student_data.email)
        )
        existing_student = result.scalar_one_or_none() 
        
        if existing_student:
            return ({'equal-emails'})
        
        new_student = Student(
            name=student_data.name,
            age=student_data.age,
            grade=student_data.grade,
            email=student_data.email
        )
        
        db.add(new_student)
        await db.flush()  

        await enrolment_crud.enrol_student_in_subject(db, student_data.subjects, new_student.std_id, student_data.admin_id)
        
        await db.commit()
        await db.refresh(new_student)
        
        print(f"{new_student.name} created with enrollments.")
        return new_student
        
    except Exception as e:
        await db.rollback()
        raise e

#Get all students
async def get_students(db: AsyncSession):
    
    result = await db.execute(select(Student).options(selectinload(Student.enrolments)))
    students = result.scalars().all()
    print("This is ",students[0].name)
    print("This is ",len(students[0].enrolments))
    print("This is ",students[0].enrolments[1].enrolment_id)
    print("This is ",students[1].name)
    print("This is ",students[1].enrolments[0].enrolment_id)
    print("This is ",students[1].enrolments[1].enrolment_id)
    print("This is ",students[1].enrolments[2].enrolment_id)
    
    output = []
    
    for s in students:
        output.append({
            "std_id": s.std_id,
            "name": s.name,
            "age": s.age,
            "grade": s.grade,
            "email": s.email,
            "enrolments": [
                {
                    "enrolment_id": e.enrolment_id,
                    "subject_id": e.subject_id,
                    "enrolment_date": e.enrolment_date,
                    "admin_id": e.admin_id,
                }
                for e in s.enrolments
            ]
        })

    #=============================================================
    # Debugging output
    # Handle the load that a single list carry 
    # Important
    #=============================================================

    return output

async def get_student_by_email(db: AsyncSession, email: str):
    result = await db.execute(select(Student).where(Student.email == email))
    student = result.scalars().first()
    return student

async def update_student(db: AsyncSession, student_data: StudentUpdate,id: str):
    print("Update student called in CRUD")
    try:
        id = int(id)
        result = await db.execute(select(Student).where(Student.id == id))
        student = result.scalars().first()
        print('hello')
        if not student:
            return None

        if student_data.name is not None:
            student.name = student_data.name
        if student_data.age is not None:
            student.age = student_data.age
        if student_data.grade is not None:
            student.grade = student_data.grade
        if student_data.email is not None:
            student.email = student_data.email

        print(f"Student fetched for update: {student.id, student.name, student.age, student.grade, student.email}")
        
        await db.commit()
        await db.refresh(student)
        return student
    except Exception as e:
        await db.rollback()
        return {"error": str(e)}, 500


async def delete_student_by_email(db: AsyncSession, email: str):

    try:
        result = await db.execute(select(Student).where(Student.email == email))
        student = result.scalars().first()

        if not student:
            return None 
        
        await db.delete(student)
        await db.commit()
        return student
        
    except Exception as e:
        await db.rollback()
        return {"error": str(e)}, 500
       


