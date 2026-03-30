import schedule
import time
import threading
from scraper import correr_scraper
from analyzer import correr_analyzer

# ============================================
# INICIO — configuración del scheduler
# ============================================

def correr_pipeline_completo():
    print("\n⏰ Scheduler ejecutando pipeline...")
    nuevas = correr_scraper()
    if nuevas > 0:
        correr_analyzer()
    else:
        print("No hay vacantes nuevas — omitiendo análisis")
    print("⏰ Pipeline completado\n")

# ============================================
# PROCESO — programar tareas
# ============================================

def iniciar_scheduler():
    schedule.every(6).hours.do(correr_pipeline_completo)
    schedule.every().day.at("08:00").do(correr_pipeline_completo)

    print("⏰ Scheduler iniciado")
    print("   Buscará vacantes cada 6 horas")
    print("   Búsqueda diaria a las 8:00 AM\n")

    while True:
        schedule.run_pending()
        time.sleep(60)

def iniciar_scheduler_background():
    thread = threading.Thread(target=iniciar_scheduler, daemon=True)
    thread.start()
    print("⏰ Scheduler corriendo en segundo plano")

# ============================================
# SALIDA — correr manualmente si se ejecuta solo
# ============================================

if __name__ == "__main__":
    print("Corriendo pipeline manualmente...")
    correr_pipeline_completo()