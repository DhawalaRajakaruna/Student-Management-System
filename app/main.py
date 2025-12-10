from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from models import student, admin
from schemas.student import StudentCreate, StudentUpdate
from schemas.admin import AdminCreate, AdminUpdate

app = FastAPI()

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



# Route to serve the homepage
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("auth/index.html", {"request": request})



######################## View Student List Page ######################
@app.get("/stdlist", response_class=HTMLResponse)
async def stdlist_page(request: Request):
    return templates.TemplateResponse("students/stdlist.html", {"request": request})


######################## Login Page ######################
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/submit-login", response_class=HTMLResponse)
async def submit_login(request: Request):
    form_data = await request.form()
    username = form_data.get("username")
    password = form_data.get("password")
    #print(f"Username: {username}, Password: {password}")
    # Here you would typically validate the username and password
    return templates.TemplateResponse("dashboard.html", {"request": request, "username": username})



######################## Register Student Page ######################
@app.get("/registerstd", response_class=HTMLResponse)
async def registerstd_page(request: Request):
    return templates.TemplateResponse("students/registerstd.html", {"request": request})


@app.post("/submit-newstd", response_class=HTMLResponse)
async def submit_newstd(request: Request):
    form_data = await request.form()
    name = form_data.get("name")
    age = form_data.get("age")
    grade = form_data.get("grade")
    email = form_data.get("email")
    #print(f"Name: {name}, Age: {age}, Grade: {grade}")
    return HTMLResponse(f"<h2>Student {name} registered successfully!</h2>")


######################## Delete Student Page ######################

@app.get("/deletestd", response_class=HTMLResponse)
async def deletestd_page(request: Request):
    return templates.TemplateResponse("students/deletestd.html", {"request": request})

@app.post("/submit-delstd", response_class=HTMLResponse)
async def submit_delstd(request: Request):
    form_data = await request.form()
    id = form_data.get("id")
    #print(f"Name: {name}, Age: {age}, Grade: {grade}")
    return HTMLResponse(f"<h2>Student with the ID num:{id} , Deleted successfully!</h2>")


######################## Update Student Page ######################
@app.get("/updatestd", response_class=HTMLResponse)
async def updatestd_page(request: Request):
    return templates.TemplateResponse("students/updatestd.html", {"request": request})

