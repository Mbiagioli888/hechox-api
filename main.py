from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

BASE_URL = "https://www.hechoxnosotros.org/"

class ExploreRequest(BaseModel):
    focus_area: str = "all"

@app.post("/explore_hecho_por_nosotros")
def explore_hecho_por_nosotros(request: ExploreRequest):
    focus_area = request.focus_area
    response = requests.get(BASE_URL)
    if response.status_code != 200:
        return {"error": "Failed to load website."}

    soup = BeautifulSoup(response.text, "html.parser")
    data = {}

    def clean_text(el):
        return el.get_text(strip=True, separator="\n") if el else "Not found."

    if focus_area in ("about", "all"):
        about_section = soup.find("section", {"id": "about"})
        data["about"] = clean_text(about_section)

    if focus_area in ("projects", "all"):
