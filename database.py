import sqlite3
from datetime import datetime

DB_NAME = "jobs.db"

def get_conexion():
    conexion = sqlite3.connect(DB_NAME)
    conexion.row_factory = sqlite3.Row
    return conexion

def crear_tablas():
    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            empresa TEXT NOT NULL,
            ubicacion TEXT,
            descripcion TEXT,
            link TEXT UNIQUE,
            fuente TEXT,
            score INTEGER DEFAULT 0,
            razon TEXT,
            vista INTEGER DEFAULT 0,
            guardada INTEGER DEFAULT 0,
            fecha_encontrada TEXT,
            fecha_analizada TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS busquedas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            vacantes_encontradas INTEGER,
            vacantes_nuevas INTEGER,
            status TEXT
        )
    """)

    conexion.commit()
    conexion.close()
    print("Base de datos lista")

def insertar_vacante(titulo, empresa, ubicacion, descripcion, link, fuente):
    conexion = get_conexion()
    cursor = conexion.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO vacantes (titulo, empresa, ubicacion, descripcion, link, fuente, fecha_encontrada)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (titulo, empresa, ubicacion, descripcion, link, fuente, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conexion.commit()
        conexion.close()
        return True
    except sqlite3.IntegrityError:
        conexion.close()
        return False

def actualizar_score(link, score, razon):
    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE vacantes 
        SET score = ?, razon = ?, fecha_analizada = ?
        WHERE link = ?
    """, (score, razon, datetime.now().strftime("%Y-%m-%d %H:%M"), link))

    conexion.commit()
    conexion.close()

def obtener_vacantes(filtro="todas", limite=50):
    conexion = get_conexion()
    cursor = conexion.cursor()

    if filtro == "top":
        cursor.execute("""
            SELECT * FROM vacantes 
            WHERE score >= 7
            ORDER BY score DESC, fecha_encontrada DESC
            LIMIT ?
        """, (limite,))
    elif filtro == "nuevas":
        cursor.execute("""
            SELECT * FROM vacantes 
            WHERE vista = 0
            ORDER BY score DESC, fecha_encontrada DESC
            LIMIT ?
        """, (limite,))
    elif filtro == "guardadas":
        cursor.execute("""
            SELECT * FROM vacantes 
            WHERE guardada = 1
            ORDER BY score DESC
            LIMIT ?
        """, (limite,))
    else:
        cursor.execute("""
            SELECT * FROM vacantes 
            ORDER BY score DESC, fecha_encontrada DESC
            LIMIT ?
        """, (limite,))

    filas = cursor.fetchall()
    conexion.close()
    return [dict(f) for f in filas]

def marcar_vista(id):
    conexion = get_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE vacantes SET vista = 1 WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

def toggle_guardada(id):
    conexion = get_conexion()
    cursor = conexion.cursor()
    cursor.execute("UPDATE vacantes SET guardada = CASE WHEN guardada = 1 THEN 0 ELSE 1 END WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

def registrar_busqueda(encontradas, nuevas, status):
    conexion = get_conexion()
    cursor = conexion.cursor()
    cursor.execute("""
        INSERT INTO busquedas (fecha, vacantes_encontradas, vacantes_nuevas, status)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().strftime("%Y-%m-%d %H:%M"), encontradas, nuevas, status))
    conexion.commit()
    conexion.close()

def obtener_stats():
    conexion = get_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) as total FROM vacantes")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as nuevas FROM vacantes WHERE vista = 0")
    nuevas = cursor.fetchone()["nuevas"]

    cursor.execute("SELECT COUNT(*) as top FROM vacantes WHERE score >= 7")
    top = cursor.fetchone()["top"]

    cursor.execute("SELECT COUNT(*) as guardadas FROM vacantes WHERE guardada = 1")
    guardadas = cursor.fetchone()["guardadas"]

    cursor.execute("SELECT fecha FROM busquedas ORDER BY id DESC LIMIT 1")
    ultima = cursor.fetchone()
    ultima_busqueda = ultima["fecha"] if ultima else "Nunca"

    conexion.close()
    return {
        "total": total,
        "nuevas": nuevas,
        "top": top,
        "guardadas": guardadas,
        "ultima_busqueda": ultima_busqueda
    }

crear_tablas()