import sqlite3

conn = sqlite3.connect("seleccion_personal.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE candidatos ADD COLUMN cargo_postula TEXT")
    print("✔ Columna cargo_postula agregada")
except:
    print("ℹ La columna cargo_postula ya existe")

conn.commit()
conn.close()
