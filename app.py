import streamlit as st
import sqlite3
import pandas as pd
import os
import hashlib
import hmac
from io import BytesIO
from referencias import modulo_referencias  # ✅ IMPORT CORRECTO
from ver_candidatos import ver_candidatos   # ✅ IMPORT CORRECTO
from editar_candidatos import editar_candidato

# ---------------- CONFIGURACIÓN ----------------
st.set_page_config(page_title="Sistema de Selección", layout="wide")
def generar_hash_password(password):
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verificar_password(password):
    password_correcto_hash = st.secrets.get("ADMIN_PASSWORD_HASH", "")
    password_ingresado_hash = generar_hash_password(password)

    return hmac.compare_digest(password_ingresado_hash, password_correcto_hash)


def login_admin():
    if "admin_autenticado" not in st.session_state:
        st.session_state.admin_autenticado = False

    if st.session_state.admin_autenticado:
        return True

    st.sidebar.markdown("---")
    st.sidebar.subheader("Acceso privado")

    password = st.sidebar.text_input(
        "Contraseña",
        type="password"
    )

    if st.sidebar.button("Ingresar"):
        if verificar_password(password):
            st.session_state.admin_autenticado = True
            st.rerun()
        else:
            st.sidebar.error("Contraseña incorrecta")

    return False


def cerrar_sesion():
    if st.session_state.get("admin_autenticado", False):
        if st.sidebar.button("Cerrar sesión"):
            st.session_state.admin_autenticado = False
            st.rerun()

    # ---------------- ESTILO PROFESIONAL ----------------
st.markdown("""
<style>

:root{
    --navy:#03045E;
    --navy-2:#06116f;
    --navy-soft:#0b1b78;
    --gold:#FDD817;
    --gold-hover:#e8c514;
    --white:#ffffff;
    --text-soft:#e5e7eb;
    --border:rgba(253,216,23,0.28);
}

/* ====== FONDO GENERAL ====== */
.stApp{
    background:var(--navy);
    color:var(--white);
}

/* Oculta la barra superior de Streamlit */
header,
[data-testid="stHeader"]{
    visibility:hidden;
    display:none;
}

.block-container{
    padding-top:1rem;
}

/* ====== SIDEBAR ====== */
section[data-testid="stSidebar"]{
    background:var(--navy) !important;
    border-right:1px solid var(--border);
}

section[data-testid="stSidebar"] *{
    color:var(--white) !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3{
    color:var(--gold) !important;
    font-weight:700;
}

section[data-testid="stSidebar"] hr{
    border-color:var(--border);
}

/* Radio Buttons */
div[role="radiogroup"] label{
    color:var(--white) !important;
    padding:10px 12px;
    border-radius:8px;
    transition:0.2s ease;
}

/* Radio Buttons */
div[role="radiogroup"] label{
    color:#ffffff !important;
    padding:10px;
    border-radius:10px;
    transition:0.2s;
}

div[role="radiogroup"] label:hover{
    background:var(--navy-soft) !important;
}

/* Texto del menú */
div[role="radiogroup"] p{
    color:var(--white) !important;
    font-size:15px;
    font-weight:600;
}

/* ====== TÍTULOS ====== */

h1{
    color:var(--gold) !important;
    font-weight:800;
}

h2,h3{
    color:var(--white) !important;
    font-weight:700;
}

/* ====== LABELS ====== */

label{
    color:var(--text-soft) !important;
    font-weight:600;
}

/* ====== INPUTS ====== */

.stTextInput input,
.stTextArea textarea,
.stNumberInput input{
    background:var(--navy-2) !important;
    color:var(--white) !important;
    border:1px solid var(--border) !important;
    border-radius:8px;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stNumberInput input:focus{
    border-color:var(--gold) !important;
    box-shadow:0 0 0 1px var(--gold) !important;
}

/* ====== SELECTBOX ====== */

.stSelectbox div[data-baseweb="select"],
.stSelectbox div[data-baseweb="select"] > div{
    background:var(--navy-2) !important;
    color:var(--white) !important;
    border:1px solid var(--border) !important;
    border-radius:8px !important;
}

.stSelectbox div[data-baseweb="select"] span,
.stSelectbox div[data-baseweb="select"] input,
.stSelectbox div[data-baseweb="select"] svg{
    color:var(--white) !important;
    fill:var(--gold) !important;
}

/* Menú desplegable del selectbox */
div[data-baseweb="popover"],
div[data-baseweb="menu"],
ul[role="listbox"],
div[role="listbox"]{
    background:var(--navy-2) !important;
    color:var(--white) !important;
    border:1px solid var(--border) !important;
}

li[role="option"],
div[role="option"]{
    background:var(--navy-2) !important;
    color:var(--white) !important;
}

li[role="option"]:hover,
div[role="option"]:hover,
li[aria-selected="true"],
div[aria-selected="true"]{
    background:var(--gold) !important;
    color:var(--navy) !important;
}

/* ====== BOTONES ====== */

.stButton>button,
.stDownloadButton>button,
.stFormSubmitButton>button{
    background:var(--gold) !important;
    color:var(--navy) !important;
    border:none !important;
    border-radius:8px !important;
    font-weight:800 !important;
    padding:10px 20px !important;
}

.stButton>button *,
.stDownloadButton>button *,
.stFormSubmitButton>button *{
    color:var(--navy) !important;
    font-weight:800 !important;
}


/* ====== DOWNLOAD BUTTON ====== */

.stButton>button:hover,
.stDownloadButton>button:hover,
button[kind="primaryFormSubmit"]:hover{
    background:var(--gold-hover) !important;
    color:var(--navy) !important;
}

/* ====== CAMPOS VACÍOS / PLACEHOLDER ====== */

input::placeholder,
textarea::placeholder{
    color:#cbd5e1 !important;
    opacity:1 !important;
}

/* Evita fondos blancos internos */
input,
textarea,
select{
    background-color:var(--navy-2) !important;
    color:var(--white) !important;
}

/* ====== TABLAS ====== */

[data-testid="stDataFrame"]{
    background:var(--navy-2) !important;
    border-radius:10px;
    border:1px solid var(--border);
}

/* ====== FORMULARIOS ====== */

div[data-testid="stForm"]{
    background:var(--navy-2);
    padding:22px;
    border-radius:10px;
    border:1px solid var(--border);
}
/* ====== MENSAJES ====== */
.stSuccess,
.stWarning,
.stInfo,
.stError{
    border-radius:8px;
}

</style>

""", unsafe_allow_html=True)

# ---------------- CONEXIÓN ----------------
conn = sqlite3.connect("seleccion_personal.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(candidatos)")
columnas_candidatos = [fila[1] for fila in cursor.fetchall()]

if "estado_evaluacion" not in columnas_candidatos:
    cursor.execute("ALTER TABLE candidatos ADD COLUMN estado_evaluacion TEXT DEFAULT 'Pendiente'")

if "comentario_interno" not in columnas_candidatos:
    cursor.execute("ALTER TABLE candidatos ADD COLUMN comentario_interno TEXT")

conn.commit()

# LOGO DE LA EMPRESA
# ===========================================================

ruta_logo = os.path.join("Assets", "logo.png")

if os.path.exists(ruta_logo):
    st.sidebar.image(ruta_logo, width=220)
else:
    st.sidebar.warning("⚠️ No se encontró el logo en Assets/logo.png")

st.sidebar.markdown("""
<div style="text-align:center;">
    <h2 style="color:white; margin-bottom:5px;">
        Sistema de Selección
    </h2>
    <p style="color:#cbd5e1; margin-top:0;">
        Departamento de Talento Humano
    </p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

# ---------------- MENÚ ----------------
st.sidebar.title("Menú")

admin_activo = login_admin()

opciones_menu = ["Registrar candidato"]

if admin_activo:
    opciones_menu += [
        "Ver candidatos",
        "Editar candidato",
        "Referencias laborales"
    ]

cerrar_sesion()

menu = st.sidebar.radio(
    "Seleccione una opción",
    opciones_menu
)

# =================================================
# ➕ REGISTRAR CANDIDATO
# =================================================
if menu == "Registrar candidato":

    st.success("Candidato registrado correctamente")

    with st.form("form_candidato"):

        st.subheader("🧑 Datos personales")
        nombre = st.text_input("Nombre completo")
        edad = st.number_input("Edad", 18, 80)
        estado_civil = st.selectbox(
            "Estado civil",
            ["Soltero/a", "Casado/a", "Unión libre", "Divorciado/a", "Viudo/a"]
        )
        hijos = st.number_input("Número de hijos", 0, 10)

        st.subheader("🎓 Formación académica")
        formacion_tercer = st.selectbox("Formación tercer nivel", ["Sí", "No"])
        titulo_cuarto = st.text_input("Título de cuarto nivel")

        st.subheader("💼 Experiencia laboral")
        anos_experiencia = st.number_input("Años de experiencia", 0, 40)
        empresa = st.text_input("Última empresa")
        cargo = st.text_input("Último cargo")
        actividades = st.text_area("Actividades realizadas")
        sueldo_ultimo = st.number_input("Último sueldo", min_value=0.0, step=10.0)
        motivo_salida = st.text_input("Motivo de salida")

        st.subheader("📌 Postulación")
        cargo_postula = st.text_input("Cargo al que postula")
        disponibilidad = st.selectbox(
            "Disponibilidad",
            ["Inmediata", "15 días", "30 días", "A convenir"]
        )

        observaciones = st.text_area("Observaciones")

        guardar = st.form_submit_button("💾 Guardar candidato")

    if guardar:
        cursor.execute("""
            INSERT INTO candidatos (
                nombre_completo,
                cargo_postula,
                edad,
                estado_civil,
                hijos,
                formacion_tercer_nivel,
                titulo_cuarto_nivel,
                anos_experiencia,
                empresa,
                cargo,
                actividades,
                sueldo_ultimo,
                motivo_salida,
                disponibilidad,
                observaciones
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nombre,
            cargo_postula,
            edad,
            estado_civil,
            hijos,
            formacion_tercer,
            titulo_cuarto,
            anos_experiencia,
            empresa,
            cargo,
            actividades,
            sueldo_ultimo,
            motivo_salida,
            disponibilidad,
            observaciones
        ))

        conn.commit()
        st.success("✅ Candidato registrado correctamente")

# =================================================
# VER CANDIDATOS
# =================================================
elif menu == "Ver candidatos":
    ver_candidatos()

# =================================================
# ✏️ EDITAR CANDIDATO
# =================================================
elif menu == "Editar candidato":
    editar_candidato()

# =================================================
# 📞 REFERENCIAS LABORALES
# =================================================
elif menu == "Referencias laborales":
    modulo_referencias()   # ✅ LLAMADA AL MÓDULO

# ---------------- CIERRE ----------------
conn.close()