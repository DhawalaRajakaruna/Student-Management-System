from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enrolment import Enrolment
from app.models.student import Student
from app.models.subject import Subject
from app.models.admin import Admin

from sqlalchemy import delete
from app.database import engine


async def initialize_default_data():
    async with AsyncSession(engine) as session:
        print("=======================================================")
        try:

            await session.execute(delete(Subject))    # Add this
            await session.execute(delete(Admin))      # Add this
            await session.commit()

            # Add subjects
            subjects = [
                Subject(sub_id=100, name="Physics", description="Into the fundamentals of matter and energy."),
                Subject(sub_id=101, name="Mathematics", description="Heart of all sciences, exploring numbers, shapes, and patterns."),
                Subject(sub_id=102, name="Chemistry", description="Chemistry unravels the secrets of substances and their transformations."),
                Subject(sub_id=103, name="Biology", description="Hunter of life, from cells to ecosystems."),
                Subject(sub_id=104, name="Art", description="Art is the soul's expression, painting emotions and stories on the canvas of life."),
            ]
            session.add_all(subjects)
            await session.flush()  # Flush to ensure subjects are inserted

            # Add admins
            admins = [
                Admin(admin_id=1, username="Dhawala", password="123", name="Dhawala Rajakaruna", email="dhawala@gmail.com"),
                Admin(admin_id=2, username="Sanka", password="456", name="Sanka Rajakaruna", email="sanka@gmail.com")
            ]
            session.add_all(admins)
            await session.flush()  # Flush to ensure admins are inserted

            await session.commit()
            print("=======================================================")

        except Exception as e:
            print(f"Error initializing default data: {e}")
            await session.rollback()