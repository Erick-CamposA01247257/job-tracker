import requests
import os
from dotenv import load_dotenv
from database import insertar_vacante, registrar_busqueda

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# ============================================
# INICIO — configuración de búsquedas
# ============================================

BUSQUEDAS = [
    "AI Developer Monterrey",
    "Python Developer Monterrey",
    "Ciberseguridad Monterrey",
    "Automatización Python México",
    "Desarrollador Python México",
]


HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

# ============================================
# PROCESO — funciones de búsqueda
# ============================================

def buscar_vacantes(query, pagina=1):
    url = "https://jsearch.p.rapidapi.com/search"
    params = {
        
    "query": query,
    "page": str(pagina),
    "num_pages": "1",
    "date_posted": "month",
    "country": "mx",
    "language": "es"

    }

    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        data = response.json()

        if "data" not in data:
            print(f"Error en respuesta: {data}")
            return []

        return data["data"]

    except Exception as e:
        print(f"Error buscando '{query}': {e}")
        return []

def limpiar_texto(texto):
    if not texto:
        return ""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(texto, "html.parser")
    return soup.get_text(separator=" ").strip()[:2000]

def procesar_vacante(vacante):
    titulo = vacante.get("job_title", "Sin título")
    empresa = vacante.get("employer_name", "Sin empresa")
    ubicacion = f"{vacante.get('job_city', '')}, {vacante.get('job_country', '')}".strip(", ")
    descripcion = limpiar_texto(vacante.get("job_description", ""))
    link = vacante.get("job_apply_link") or vacante.get("job_url", "")
    fuente = vacante.get("job_publisher", "JSearch")

    return {
        "titulo": titulo,
        "empresa": empresa,
        "ubicacion": ubicacion,
        "descripcion": descripcion,
        "link": link,
        "fuente": fuente
    }

# ============================================
# SALIDA — función principal
# ============================================

def correr_scraper():
    print("\n🔍 Iniciando búsqueda de vacantes...")
    total_encontradas = 0
    total_nuevas = 0

    for query in BUSQUEDAS:
        print(f"   Buscando: {query}")
        resultados = buscar_vacantes(query)

        for resultado in resultados:
            vacante = procesar_vacante(resultado)

            if not vacante["link"]:
                continue

            total_encontradas += 1
            es_nueva = insertar_vacante(
                vacante["titulo"],
                vacante["empresa"],
                vacante["ubicacion"],
                vacante["descripcion"],
                vacante["link"],
                vacante["fuente"]
            )

            if es_nueva:
                total_nuevas += 1
                print(f"   ✅ Nueva: {vacante['titulo']} — {vacante['empresa']}")

    registrar_busqueda(total_encontradas, total_nuevas, "ok")
    print(f"\n✅ Búsqueda completada — {total_encontradas} encontradas, {total_nuevas} nuevas\n")
    return total_nuevas

if __name__ == "__main__":
    correr_scraper()