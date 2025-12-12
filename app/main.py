from pathlib import Path
from fastapi import FastAPI, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession


from database import engine, Base, get_db

# Import ALL models so they register with Base.metadata
from models.student import Student
from models.admin import Admin
from models.enrolment import Enrolment
from models.subject import Subject

from schemas.student import StudentCreate,StudentRead, StudentUpdate
from schemas.admin import AdminCreate, AdminUpdate, AdminRead, AdminLogin
from typing import List

from crud import student as student_crud
from crud import admin as admin_crud
from crud import subject as subject_crud

# Middleware for session management
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

#just for future use cases like flash messages , user sessions etc.
app.add_middleware(
    SessionMiddleware, 
    secret_key="A7x9K2mP5qR8sT1vW4yZ7bC0dF3gH6jL9nM2pQ5rS8tU1vX4wY7zA0bC3dE6fG"
)

#Create all the database tables when it starts
@app.on_event("startup")# make it run when application starts 
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully.")   


# Get the directory where main.py is located
BASE_DIR = Path(__file__).resolve().parent

# Initialize Jinja2 templates with absolute path
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

#No need of having satics files for now
#app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

######################### Home Page ######################
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("auth/index.html", {"request": request})


######################## View Student List Page ######################
@app.get("/stdlist", response_class=HTMLResponse)
async def stdlist_page(request: Request):
    return templates.TemplateResponse("students/stdlist.html", {"request": request})

@app.get("/get-all-students", response_model=List[StudentRead])
async def get_all_students(db: AsyncSession = Depends(get_db)):
    students = await student_crud.get_students(db)
    print("new ew neww")
    return students

@app.get("/get-students-by-mail", response_class=JSONResponse)
async def get_students_by_mail(email: str, db: AsyncSession = Depends(get_db)):
    student = await student_crud.get_student_by_email(db, email) #calling the crud function
    if student:
        return JSONResponse(content={ # returning json response to the frontend
            "std_id": student.std_id,
            "name": student.name,
            "age": student.age,
            "grade": student.grade,
            "email": student.email
        })
    else:
        return JSONResponse(content={"error": "Student not found"}, status_code=404)



######################## Register Student Page ######################
@app.get("/registerstd", response_class=HTMLResponse)
async def registerstd_page(request: Request, db: AsyncSession = Depends(get_db)):
    subjects = await subject_crud.get_all_subjects(db)
    
    #return templates.TemplateResponse("students/registerstd.html", {"request": request})
    return templates.TemplateResponse(
        "students/registerstd.html", 
        {"request": request, "subjects": subjects}
    )

@app.post("/submit-newstd", response_class=HTMLResponse)
async def submit_newstd(request: Request, db: AsyncSession = Depends(get_db)):
    
    admin_id = request.session.get("admin_id")

    try:
        form_data = await request.form()
        name = form_data.get("name")
        age = form_data.get("age")
        grade = form_data.get("grade")
        email = form_data.get("email")

        subjects = form_data.getlist("subjects")

        # Validation
        try:
            age_int = int(age)
            if age_int <= 0 or age_int > 150:
                return HTMLResponse("<h2>Error: Invalid age value!</h2>", status_code=400)
        except ValueError:
            return HTMLResponse("<h2>Error: Age must be a number!</h2>", status_code=400)

        student_data = StudentCreate(
            name=name,
            age=age_int,
            grade=grade,
            email=email,
            subjects=subjects,
            admin_id=admin_id
        )
        #print(student_data.name)
        
        result = await student_crud.create_student(db, student_data)
        if result == {'equal-emails'}:
            return HTMLResponse("""
                <script>
                    alert('Student with this email already exists!');
                    window.history.back();
                </script>
            """)
        return HTMLResponse(f"<h2>Student {name} registered successfully!</h2>")
        
    except Exception as e:
        return HTMLResponse(f"<h2>Error registering student: {str(e)}</h2>", status_code=500)


######################## Delete Student Page ######################

@app.get("/deletestd", response_class=HTMLResponse)
async def deletestd_page(request: Request):
    return templates.TemplateResponse("students/deletestd.html", {"request": request})

@app.post("/submit-delstd", response_class=HTMLResponse)
async def submit_delstd(request: Request, db: AsyncSession = Depends(get_db)):
    form_data = await request.form()
    email = form_data.get("email")

    await student_crud.delete_student_by_email(db, email)
    return HTMLResponse(f"<h2>Student with the ID num:{id} , Deleted successfully!</h2>")


######################## Update Student Page ######################
@app.get("/updatestd", response_class=HTMLResponse)
async def updatestd_page(request: Request):
    return templates.TemplateResponse("students/updatestd.html", {"request": request})

@app.post("/submit-updatestd", response_class=HTMLResponse)
async def submit_updatestd(request: Request,db: AsyncSession = Depends(get_db)):

    try:
        form_data = await request.form()
        id = form_data.get("id")
        name = form_data.get("name")
        age = form_data.get("age")
        grade = form_data.get("grade")
        email = form_data.get("email")


        try:
            age_int = int(age)
            if age_int <= 0 or age_int > 150:
                return HTMLResponse("<h2>Error: Invalid age value!</h2>", status_code=400)
        except ValueError:
            return HTMLResponse("<h2>Error: Age must be a number!</h2>", status_code=400)

        student_data = StudentUpdate(
            name=name,
            age=age_int,
            grade=grade,
            email=email
        )
        
        await student_crud.update_student(db, student_data,id)
        return HTMLResponse(f"<h2>Student {name} registered successfully!</h2>")
        
    except Exception as e:
        return HTMLResponse(f"<h2>Error registering student: {str(e)}</h2>", status_code=500)



######################## Login Page ######################
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/submit-login", response_class=HTMLResponse)
async def submit_login(request: Request,db: AsyncSession = Depends(get_db)):
    try:
        form_data = await request.form()
        username = form_data.get("username")
        password = form_data.get("password")
        
        log_admin = AdminLogin(username=username, password=password)
        isadmin = await admin_crud.login_admin(db, log_admin)

        if isadmin is None:
            return HTMLResponse("<h2>Invalid username or password!</h2>", status_code=401)
        # Use session to store admin info
        request.session["admin_id"] = isadmin.admin_id if isadmin else None

        return templates.TemplateResponse("dashboard.html", {"request": request, "username": username})
    except Exception as e:
        return HTMLResponse(f"<h2>Error during login: {str(e)}</h2>", status_code=500)
