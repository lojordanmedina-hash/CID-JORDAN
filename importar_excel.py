import sqlite3
import pandas as pd
import os

RUTA_DB = "seleccion_personal.db"
CARPETA_EXCEL = "data/excels_originales"

def importar_excels():
    conn = sqlite3.connect(RUTA_DB)
    cursor = conn.cursor()

    archivos = [
        f for f in os.listdir(CARPETA_EXCEL)
        if f.endswith(".xlsx") and not f.startswith("~$")
    ]

    total = 0

    for archivo in archivos:
        ruta = os.path.join(CARPETA_EXCEL, archivo)
        print(f"📄 Procesando: {archivo}")

        df = pd.read_excel(
            ruta,
            sheet_name="MÉDICO VALLE",
            header=4,              # ✅ FILA CORRECTA
            engine="openpyxl"
        )

        # Limpieza de columnas
        df.columns = df.columns.str.strip()

        for _, row in df.iterrows():

            if pd.isna(row.get("Candidato/a")):
                continue

            try:
                aspiracion = float(
                    str(row.get("Aspiración salarial", 0))
                    .replace("$", "")
                    .replace(",", "")
                )
            except:
                aspiracion = 0.0

            cursor.execute("""
                INSERT INTO candidatos (
                    nombre_completo,
                    edad,
                    estado_civil,
                    formacion_tercer_nivel,
                    anos_experiencia,
                    aspiracion_salarial,
                    disponibilidad,
                    observaciones
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row.get("Candidato/a"),
                row.get("Edad"),
                row.get("Estado Civil"),
                row.get("Título Tercer Nivel"),
                row.get("Años de experiencia\n(Total en el área) "),
                aspiracion,
                row.get("Disponibilidad"),
                row.get("Observaciones")
            ))

            total += 1

    conn.commit()
    conn.close()

    print(f"✅ Importación completada: {total} candidatos cargados")

if __name__ == "__main__":
    importar_excels()
