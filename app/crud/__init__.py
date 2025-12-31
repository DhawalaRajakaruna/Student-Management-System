from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.database import engine
from app.models.subject import Subject
from app.models.admin import Admin
from dotenv import load_dotenv
import os
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent
# ENV_PATH = BASE_DIR / ".env"

# load_dotenv(dotenv_path=ENV_PATH)
load_dotenv()

async def initialize_default_data():
    async with AsyncSession(engine) as session:
        print("=======================================================")
        try:
            await session.execute(delete(Subject))
            await session.execute(delete(Admin))
            await session.commit()


            subjects = [
                Subject(sub_id=100, name="Physics", description="Into the fundamentals of matter and energy."),
                Subject(sub_id=101, name="Mathematics", description="Heart of all sciences, exploring numbers, shapes, and patterns."),
                Subject(sub_id=102, name="Chemistry", description="Chemistry unravels the secrets of substances and their transformations."),
                Subject(sub_id=103, name="Biology", description="Hunter of life, from cells to ecosystems."),
                Subject(sub_id=104, name="Art", description="Art is the soul's expression, painting emotions and stories on the canvas of life."),
            ]
            session.add_all(subjects)
            await session.flush()


            admins = []
            for i in range(1, 3):  
                admin_id = int(os.getenv(f"ADMIN{i}_ID"))
                username = os.getenv(f"ADMIN{i}_USERNAME")
                password = os.getenv(f"ADMIN{i}_PASSWORD")
                name = os.getenv(f"ADMIN{i}_NAME")
                email = os.getenv(f"ADMIN{i}_EMAIL")
                admins.append(Admin(admin_id=admin_id, username=username, password=password, name=name, email=email))
            
            session.add_all(admins)
            await session.flush()

            await session.commit()
            print("Default data initialized successfully.")
            print("=======================================================")

        except Exception as e:
            print(f"Error initializing default data: {e}")
            await session.rollback()
