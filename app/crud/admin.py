from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.admin import Admin
from schemas.admin import AdminCreate, AdminUpdate, AdminLogin

async def login_admin(db: AsyncSession, admin_data: AdminLogin):
    try:
        result = await db.execute(select(Admin).where(Admin.username == admin_data.username, Admin.password == admin_data.password))
        admin = result.scalars().first()
        return admin
    except Exception as e:
        return ({"error": str(e)}, 500)