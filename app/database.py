from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import configparser
from pathlib import Path

import asyncio
from sqlalchemy import text

config = configparser.ConfigParser()
config_path = Path(__file__).resolve().parent / 'database.ini'
config.read(config_path)

db_user = config['postgresql']['user']
db_password = config['postgresql']['password'] 
db_host = config['postgresql']['host']
db_port = config['postgresql']['port']

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/managedb"

print(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

Base = declarative_base()

async def get_db():
     async with AsyncSessionLocal() as session:
         yield session

# async def test_connection():
#     try:
#         async with engine.connect() as conn:
#             result = await conn.execute(text("SELECT 1"))
#             print("Database connected successfully!")
#     except Exception as e:
#         print("Database connection failed:")
#         print(e)

# if __name__ == "__main__":
#     # Test the database connection
#     asyncio.run(test_connection())