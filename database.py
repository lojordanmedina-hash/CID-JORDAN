import sqlite3

def crear_base_de_datos():
    conn = sqlite3.connect("seleccion_personal.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mbti_info (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_letras TEXT UNIQUE,
        significado TEXT,
        descripcion TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidatos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_completo TEXT,
        edad INTEGER,
        estado_civil TEXT,
        formacion_tercer_nivel TEXT,
        anos_experiencia TEXT,
        aspiracion_salarial REAL,
        disponibilidad TEXT,
        observaciones TEXT,
        estado_proceso TEXT DEFAULT 'ACTIVO'
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS evaluaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidato_id INTEGER,
        conocimientos_score REAL,
        personalidad_mbti TEXT,
        impedimento_legal BOOLEAN,
        referencias_check BOOLEAN,
        FOREIGN KEY (candidato_id) REFERENCES candidatos(id)
    )
    """)

    conn.commit()
    conn.close()
    print("✅ Base de datos creada correctamente")

if __name__ == "__main__":
    crear_base_de_datos()
