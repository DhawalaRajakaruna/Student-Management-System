from pathlib import Path
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request

# Initialize FastAPI app
app = FastAPI()

# Get the directory where main.py is located
BASE_DIR = Path(__file__).resolve().parent

# Initialize Jinja2 templates with absolute path
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Route to serve the homepage
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Render the HTML template
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html",{"request": request})

@app.get("/registerstd", response_class=HTMLResponse)
async def registerstd_page(request: Request):
    return templates.TemplateResponse("registerstd.html",{"request": request})

@app.get("/stdlist", response_class=HTMLResponse)
async def stdlist_page(request: Request):
    return templates.TemplateResponse("stdlist.html",{"request": request})