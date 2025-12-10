from pydantic import BaseModel

class StudentCreate(BaseModel): # Use to Add new student (Save )
    name: str   # All fields required
    age: int    # must send all fields   
    grade: str
    email: str

class StudentUpdate(BaseModel): #Use to update students
    name: str | None = None
    age: int | None = None # this measn those fields are optional
    grade: str | None = None# can be eather with balues or not 
    email: str | None = None# Since it is to update waht we want


    
