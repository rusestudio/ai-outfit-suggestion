import logging as log
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse , FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from data_to_be_prompt import clothes_data
from llm_model_suggest import main as llm_main
from google_weather import get_weather


# ---------------- LOG SETUP ----------------
def setup_log():
    log.basicConfig(
        level=log.INFO,
        format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        handlers=[
            log.FileHandler('server.log'),
            log.StreamHandler()
        ]
    )

setup_log()
logger = log.getLogger(__name__)


# ---------------- FASTAPI SETUP ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app = FastAPI()


# ---------------- ROUTES ----------------
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# ---------------- REQUEST MODELS ----------------
class SubmitData(BaseModel):
    when: str
    destination: str
    environment: str


class Location(BaseModel):
    latitude: float
    longitude: float


class SubmitRequest(BaseModel):
    submit_data: SubmitData
    location: Location


# ---------------- MAIN GENERATION ENDPOINT ----------------
@app.post("/submit")
async def submit_form(submit: SubmitRequest, request: Request):

    try:
        user_input = submit.submit_data.dict()

        lat = submit.location.latitude
        lon = submit.location.longitude

        # 🔥 NEW: Google-based weather
        weather_data = get_weather(lat, lon)

        # Stateless user (no login)
        user_data = {}

        suggestions = llm_main(
            user_data,
            weather_data,
            clothes_data,
            user_input
        )

        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "suggestions": suggestions,
            }
        )

    except Exception as e:
        logger.error(f"Submit error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{filename}")
def download_image(filename: str):
    file_path = os.path.join("api_out", "txt2img", filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(
        file_path,
        media_type="image/png",
        filename=filename
    )
