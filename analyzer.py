import anthropic
import json
from dotenv import load_dotenv
from database import obtener_vacantes, actualizar_score

load_dotenv()

client = anthropic.Anthropic()

# ============================================
# INICIO — perfil de Erick para comparar
# ============================================

PERFIL = """
Nombre: Erick Giovani Campos Aguirre
Ubicación: Monterrey, Nuevo León, México
Graduación: Julio 2026 — Ingeniería en Robótica y Sistemas Digitales, Tec de Monterrey
Concentración: Ciberseguridad

Habilidades técnicas:
- Python (intermedio), C++, SQL, JavaScript
- Claude API, LangChain, ChromaDB, RAG, Tool Calling, Prompt Engineering
- FastAPI, Flask, Uvicorn, Pydantic
- SQLite, bases de datos relacionales
- Git, GitHub, Linux
- TCP/IP, VLANs, NIST RMF, ISO 27001
- AWS Cloud Foundations

Proyectos construidos:
- Research Agent: agente autónomo con tool calling y FastAPI
- RAG Chatbot: pipeline completo con LangChain y ChromaDB
- Finance Tracker: app web con SQLite, FastAPI y Claude API
- Chatbot con memoria: Flask + Claude API

Certificaciones:
- Cisco CyberOps Associate
- AWS Cloud Foundations
- ISC2 CC (en progreso)

Inglés: Avanzado
Experiencia formal: 0 años (estudiante a punto de graduarse)
Disponibilidad: Tiempo completo o freelance
"""

# ============================================
# PROCESO — analizar una vacante con Claude
# ============================================

def analizar_vacante(vacante):
    if not vacante.get("descripcion"):
        return 0, "Sin descripción disponible para analizar"

    prompt = f"""Analiza qué tan bien esta vacante de trabajo coincide con el perfil del candidato.

PERFIL DEL CANDIDATO:
{PERFIL}

VACANTE:
Título: {vacante['titulo']}
Empresa: {vacante['empresa']}
Ubicación: {vacante['ubicacion']}
Descripción: {vacante['descripcion'][:1500]}

Evalúa y responde ÚNICAMENTE con un JSON válido con esta estructura exacta:
{{
    "score": <número del 1 al 10>,
    "razon": "<explicación breve de 2-3 oraciones de por qué el score>"
}}

Criterios de scoring:
- 9-10: Coincidencia excelente, aplica inmediatamente
- 7-8: Buena coincidencia, vale la pena aplicar
- 5-6: Coincidencia parcial, requiere aprender algo nuevo
- 3-4: Poca coincidencia pero relacionado
- 1-2: No relacionado con el perfil

No incluyas nada más que el JSON. Sin explicaciones adicionales."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        texto = response.content[0].text.strip()
        texto = texto.replace("```json", "").replace("```", "").strip()
        resultado = json.loads(texto)

        score = int(resultado.get("score", 0))
        razon = resultado.get("razon", "Sin análisis")

        return score, razon

    except Exception as e:
        print(f"Error analizando vacante: {e}")
        return 0, "Error en el análisis"

# ============================================
# SALIDA — función principal
# ============================================

def correr_analyzer():
    print("\n🧠 Iniciando análisis de vacantes...")

    vacantes = obtener_vacantes(filtro="todas")
    sin_analizar = [v for v in vacantes if v["score"] == 0]

    if not sin_analizar:
        print("No hay vacantes nuevas para analizar")
        return 0

    print(f"   Vacantes por analizar: {len(sin_analizar)}")
    analizadas = 0

    for vacante in sin_analizar:
        print(f"   Analizando: {vacante['titulo']} — {vacante['empresa']}")
        score, razon = analizar_vacante(vacante)
        actualizar_score(vacante["link"], score, razon)

        emoji = "🔥" if score >= 9 else "✅" if score >= 7 else "⚠️" if score >= 5 else "❌"
        print(f"   {emoji} Score: {score}/10 — {razon[:80]}...")
        analizadas += 1

    print(f"\n✅ Análisis completado — {analizadas} vacantes analizadas\n")
    return analizadas

if __name__ == "__main__":
    correr_analyzer()