from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from database import obtener_vacantes, obtener_stats, marcar_vista, toggle_guardada
from scraper import correr_scraper
from analyzer import correr_analyzer
from scheduler import iniciar_scheduler_background

load_dotenv()

app = FastAPI()

iniciar_scheduler_background()

class AccionVacante(BaseModel):
    id: int

@app.get("/", response_class=HTMLResponse)
async def index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/vacantes")
async def listar_vacantes(filtro: str = "todas"):
    return obtener_vacantes(filtro=filtro)

@app.get("/stats")
async def stats():
    return obtener_stats()

@app.post("/vacante/vista")
async def marcar_vacante_vista(accion: AccionVacante):
    marcar_vista(accion.id)
    return {"status": "ok"}

@app.post("/vacante/guardar")
async def guardar_vacante(accion: AccionVacante):
    toggle_guardada(accion.id)
    return {"status": "ok"}

@app.post("/buscar")
async def buscar_ahora():
    nuevas = correr_scraper()
    if nuevas > 0:
        correr_analyzer()
    return {"status": "ok", "nuevas": nuevas}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)