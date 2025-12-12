from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.enrolment import Enrolment

async def enrol_student_in_subject(db: AsyncSession, sub_ids: list, std_id: int, admin_id: int):
    for sub_id in sub_ids:
        new_enrollment = Enrolment(
            student_id=std_id,
            subject_id=int(sub_id),
            admin_id=admin_id,
            enrolment_date="None"  # Set default value (can be updated later
        )
        db.add(new_enrollment)