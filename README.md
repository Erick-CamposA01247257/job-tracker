# 🎯 Job Tracker — AI-Powered Job Search Automation

Automated job search system that finds, stores, and scores job vacancies using Claude AI. Runs automatically every 6 hours without any manual intervention.

## What it does

- Searches for new job vacancies every 6 hours automatically
- Stores all vacancies in a SQLite database without duplicates
- Uses Claude AI to score each vacancy from 1 to 10 based on your profile
- Shows a dashboard with vacancies ordered by score
- Lets you filter by unseen, top score, or saved vacancies
- Manual search button to trigger a search without waiting

## Technologies

- Python 3.12
- FastAPI
- Claude API (Anthropic) — vacancy scoring
- JSearch API (RapidAPI) — vacancy data
- SQLite — local database
- BeautifulSoup4 — HTML cleaning
- Schedule — background task scheduling
- Uvicorn

## Installation

1. Clone the repository:
git clone https://github.com/Erick-CamposA01247257/job-tracker.git

2. Install dependencies:
pip install -r requirements.txt

3. Create a .env file with your API keys:
ANTHROPIC_API_KEY=your_anthropic_key
RAPIDAPI_KEY=your_rapidapi_key

4. Run the app:
uvicorn app:app --reload

5. Open in your browser:
http://localhost:8000

## Architecture

- scraper.py — fetches vacancies from JSearch API
- analyzer.py — scores each vacancy using Claude AI
- database.py — handles all SQLite operations
- scheduler.py — runs the pipeline every 6 hours automatically
- app.py — FastAPI server and endpoints
- templates/index.html — dashboard UI

## Author

Erick Campos — Tec de Monterrey


# 🎯 Job Tracker — Búsqueda de Empleo Automatizada con IA

Sistema automatizado de búsqueda de empleo que encuentra, guarda y puntúa vacantes usando Claude AI. Corre automáticamente cada 6 horas sin ninguna intervención manual.

## ¿Qué hace?

- Busca vacantes nuevas cada 6 horas automáticamente
- Guarda todas las vacantes en SQLite sin duplicados
- Usa Claude AI para puntuar cada vacante del 1 al 10 según tu perfil
- Muestra un dashboard con las vacantes ordenadas por score
- Permite filtrar por no vistas, score alto o guardadas
- Botón de búsqueda manual para no esperar las 6 horas

## Tecnologías

- Python 3.12
- FastAPI
- Claude API (Anthropic) — puntuación de vacantes
- JSearch API (RapidAPI) — datos de vacantes
- SQLite — base de datos local
- BeautifulSoup4 — limpieza de HTML
- Schedule — tareas automáticas en segundo plano
- Uvicorn

## Instalación

1. Clona el repositorio:
git clone https://github.com/Erick-CamposA01247257/job-tracker.git

2. Instala las dependencias:
pip install -r requirements.txt

3. Crea un archivo .env con tus API keys:
ANTHROPIC_API_KEY=tu_key_de_anthropic
RAPIDAPI_KEY=tu_key_de_rapidapi

4. Corre la app:
uvicorn app:app --reload

5. Abre en tu navegador:
http://localhost:8000

## Arquitectura

- scraper.py — obtiene vacantes de JSearch API
- analyzer.py — puntúa cada vacante con Claude AI
- database.py — maneja todas las operaciones SQLite
- scheduler.py — corre el pipeline cada 6 horas automáticamente
- app.py — servidor FastAPI y endpoints
- templates/index.html — interfaz del dashboard

## Autor

Erick Campos — Tec de Monterrey