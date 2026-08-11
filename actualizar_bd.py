import sqlite3

conn = sqlite3.connect("seleccion_personal.db")
cursor = conn.cursor()

# Agregar columnas si no existen
columnas = {
    "hijos": "INTEGER",
    "titulo_cuarto_nivel": "TEXT",
    "anos_experiencia": "TEXT",
    "empresa": "TEXT",
    "cargo": "TEXT",
    "actividades": "TEXT",
    "sueldo_ultimo": "REAL",
    "motivo_salida": "TEXT",
    "disponibilidad": "TEXT"
}

for columna, tipo in columnas.items():
    try:
        cursor.execute(f"ALTER TABLE candidatos ADD COLUMN {columna} {tipo}")
        print(f"✔ Columna agregada: {columna}")
    except:
        pass  # ya existe

conn.commit()
conn.close()

print("✅ Base de datos actualizada correctamente")
