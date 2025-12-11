from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.student import Student
from schemas.student import StudentCreate, StudentUpdate

#Create Student
async def create_student(db: AsyncSession, student_data: StudentCreate):
    #reate a new student instance and add an ID for it
    try:
        new_student = Student(
            name=student_data.name,
            age=student_data.age,
            grade=student_data.grade,
            email=student_data.email
        )
        db.add(new_student)
        await db.commit()
        await db.refresh(new_student)
        return new_student
    except Exception as e:
        await db.rollback()
        return ({"error": str(e)}, 500)

#Get all students
async def get_students(db: AsyncSession):
    result = await db.execute(select(Student))
    students = result.scalars().all()
    return students

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
       


