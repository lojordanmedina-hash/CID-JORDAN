import os
import sqlite3
import pandas as pd
import streamlit as st


DB_PATH = os.path.join(os.path.dirname(__file__), "seleccion_personal.db")


def asegurar_columnas_evaluacion(conn):
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(candidatos)")
    columnas = [fila[1] for fila in cursor.fetchall()]

    if "estado_evaluacion" not in columnas:
        cursor.execute("ALTER TABLE candidatos ADD COLUMN estado_evaluacion TEXT DEFAULT 'Pendiente'")

    if "comentario_interno" not in columnas:
        cursor.execute("ALTER TABLE candidatos ADD COLUMN comentario_interno TEXT")

    cursor.execute("""
        UPDATE candidatos
        SET estado_evaluacion = 'Pendiente'
        WHERE estado_evaluacion IS NULL OR estado_evaluacion = ''
    """)

    conn.commit()


def tabla_existe(conn, tabla):
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name = ?",
        (tabla,)
    )
    return cursor.fetchone() is not None


def eliminar_candidato(conn, candidato_id):
    cursor = conn.cursor()

    for tabla in ["referencias", "evaluaciones"]:
        if tabla_existe(conn, tabla):
            cursor.execute(f"DELETE FROM {tabla} WHERE candidato_id = ?", (candidato_id,))

    cursor.execute("DELETE FROM candidatos WHERE id = ?", (candidato_id,))
    conn.commit()


def editar_candidato():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    asegurar_columnas_evaluacion(conn)

    df = pd.read_sql("""
        SELECT *
        FROM candidatos
        ORDER BY id DESC
    """, conn)

    st.title("Editar candidato")

    if df.empty:
        st.warning("No hay candidatos registrados")
        conn.close()
        return

    df["nombre_selector"] = df.apply(
        lambda fila: f"{fila['id']} - {fila['nombre_completo']} - {fila.get('cargo_postula', '')}",
        axis=1
    )

    candidato_seleccionado = st.selectbox(
        "Seleccione un candidato",
        df["nombre_selector"]
    )

    candidato_id = int(candidato_seleccionado.split(" - ")[0])
    fila = df[df["id"] == candidato_id].iloc[0]

    with st.form("editar"):

        edad = st.number_input(
            "Edad",
            min_value=18,
            max_value=80,
            value=int(fila["edad"]) if pd.notnull(fila["edad"]) else 18
        )

        estado = st.text_input(
            "Estado civil",
            fila["estado_civil"] if pd.notnull(fila["estado_civil"]) else ""
        )

        cargo_postula = st.text_input(
            "Cargo al que postula",
            fila["cargo_postula"] if pd.notnull(fila["cargo_postula"]) else ""
        )

        experiencia = st.number_input(
            "Años experiencia",
            min_value=0,
            max_value=40,
            value=int(fila["anos_experiencia"]) if pd.notnull(fila["anos_experiencia"]) else 0
        )

        observaciones = st.text_area(
            "Observaciones",
            fila["observaciones"] if pd.notnull(fila["observaciones"]) else ""
        )

        estado_actual = (
            fila["estado_evaluacion"]
            if pd.notnull(fila["estado_evaluacion"])
            else "Pendiente"
        )

        opciones_estado = ["Pendiente", "Apto", "No apto"]

        estado_evaluacion = st.selectbox(
            "Estado de evaluación",
            opciones_estado,
            index=opciones_estado.index(estado_actual)
            if estado_actual in opciones_estado else 0
        )

        comentario_interno = st.text_area(
            "Comentario interno",
            fila["comentario_interno"]
            if pd.notnull(fila["comentario_interno"])
            else ""
        )

        guardar = st.form_submit_button("Guardar cambios")

    if guardar:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE candidatos SET
                edad = ?,
                estado_civil = ?,
                cargo_postula = ?,
                anos_experiencia = ?,
                observaciones = ?,
                estado_evaluacion = ?,
                comentario_interno = ?
            WHERE id = ?
        """, (
            edad,
            estado,
            cargo_postula,
            experiencia,
            observaciones,
            estado_evaluacion,
            comentario_interno,
            candidato_id
        ))

        conn.commit()
        st.success("Candidato actualizado correctamente")
        st.rerun()

    st.divider()
    st.subheader("Eliminar candidato")
    st.warning("Esta accion eliminara el candidato seleccionado y sus registros asociados.")

    confirmar_eliminacion = st.checkbox(
        f"Confirmo que deseo eliminar a {fila['nombre_completo']}",
        key=f"confirmar_eliminar_{candidato_id}"
    )

    if st.button(
        "Eliminar candidato",
        disabled=not confirmar_eliminacion,
        key=f"eliminar_{candidato_id}"
    ):
        eliminar_candidato(conn, candidato_id)
        conn.close()
        st.success("Candidato eliminado correctamente")
        st.rerun()

    conn.close()
