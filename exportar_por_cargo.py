import streamlit as st
import sqlite3
import pandas as pd
import io

st.set_page_config(page_title="Exportar por cargo", layout="wide")

conn = sqlite3.connect("seleccion_personal.db", check_same_thread=False)

df = pd.read_sql("SELECT * FROM candidatos", conn)

st.title("📤 Exportar candidatos por cargo")

cargo = st.selectbox(
    "Seleccione cargo",
    df["cargo_postula"].dropna().unique()
)

df_filtrado = df[df["cargo_postula"] == cargo]

st.dataframe(df_filtrado, use_container_width=True)

buffer = io.BytesIO()
df_filtrado.to_excel(buffer, index=False, engine="openpyxl")

st.download_button(
    label="⬇️ Descargar Excel del cargo",
    data=buffer,
    file_name=f"candidatos_{cargo}.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

conn.close()
