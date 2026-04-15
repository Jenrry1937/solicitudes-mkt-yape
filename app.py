import streamlit as st
import pandas as pd
from datetime import datetime
import requests

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Canal de Solicitudes Data - Yape", layout="wide")

# --- ESTILO "YAPE VIBE" ---
st.markdown("""
    <style>
    .stApp {
        background-color: #7422ed;
        color: white;
    }
    .main-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 15px;
        color: #333;
    }
    .stButton>button {
        background-color: #00d1e5;
        color: white;
        border-radius: 20px;
        width: 100%;
        border: none;
        font-weight: bold;
    }
    /* Estilo para los inputs */
    label { color: white !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- ESTADO DE LA NAVEGACIÓN ---
if 'page' not in st.session_state:
    st.session_state.page = 'HOME'
if 'canal' not in st.session_state:
    st.session_state.canal = None

# --- FUNCIONES DE NAVEGACIÓN ---
def go_to(page, canal=None):
    st.session_state.page = page
    st.session_state.canal = canal

# --- PANTALLA: HOME ---
if st.session_state.page == 'HOME':
    st.title("¡Bienvenido!")
    st.subheader("Al Canal de Solicitudes de Data - Mkt & Growth")
    
    col1, col2 = st.columns([2, 1])
    with col2:
        if st.button("Nueva Solicitud - Base"): go_to('SELECTOR')
        if st.button("Nueva Solicitud - Análisis"): st.info("Próximamente")
        if st.button("Vista Solicitudes"): go_to('LISTA')

# --- PANTALLA: SELECTOR DE CANAL ---
elif st.session_state.page == 'SELECTOR':
    if st.button("⬅️ Atrás"): go_to('HOME')
    st.write("### Selecciona el canal para su solicitud:")
    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1: 
        if st.button("Own"): go_to('FORM', 'OWN')
    with col_c2: 
        if st.button("Paid"): go_to('FORM', 'PAID')
    with col_c3: 
        if st.button("Real State"): go_to('FORM', 'REAL STATE')

# --- PANTALLA: FORMULARIOS DINÁMICOS ---
elif st.session_state.page == 'FORM':
    canal = st.session_state.canal
    st.title(f"Canal de Solicitudes Data - {canal}")
    
    if st.button("⬅️ Volver al Selector"): go_to('SELECTOR')

    with st.container():
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        
        # CAMPOS COMUNES
        col1, col2 = st.columns(2)
        with col1:
            responsable = st.text_input("RESPONSABLE ENVIO", value="JENRRY SAMUEL PALLARCO PUCLLA", disabled=True)
            canal_impacto = st.selectbox("CANAL IMPACTO", ["Push", "Email", "SMS", "Inapp", "Meta", "TikTok", "Google", "Banner"])
            tipo_usuario = st.selectbox("TIPO USUARIO", ["Nuevo", "Recurrente", "Churn"])
        
        with col2:
            producto = st.selectbox("PRODUCTO", ["Yape", "Tienda", "Micronegocios", "Créditos"])
            tipo_comunicacion = st.selectbox("TIPO COMUNICACION", ["Informativa", "Promocional", "Test"])
            
            # Lógica condicional por canal
            if canal == 'OWN' or canal == 'REAL STATE':
                tipo_funnel = st.selectbox("TIPO FUNNEL", ["Awareness", "Conversion", "Retention"])
                deadline = st.date_input("FECHA DEADLINE")
            
            if canal == 'PAID':
                estrategia = st.selectbox("ESTRATEGIA", ["Branding", "Performance"])
                var_test = st.selectbox("VARIABLE TEST", ["Creatividad", "Audiencia", "Copy"])
                f_inicio = st.date_input("FECHA INICIO CAMPAÑA")
                f_fin = st.date_input("FECHA FIN CAMPAÑA")

        # Campos de texto
        nombre_campana = st.text_input("NOMBRE CAMPAÑA")
        if canal == 'PAID':
            ruta_paid = st.text_input("RUTA PAID")
        if canal == 'REAL STATE':
            segment_label = st.text_input("SEGMENT LABEL")
            
        descripcion = st.text_area("DESCRIPCIÓN")
        
        if canal == 'PAID':
            hipotesis = st.text_area("HIPOTESIS")

        if st.button("Guardar"):
            # AQUÍ SE CONECTARÁ CON EL WEBHOOK DE POWER AUTOMATE
            st.success(f"Solicitud para {nombre_campana} enviada correctamente a SharePoint.")
            go_to('LISTA')
            
        st.markdown('</div>', unsafe_allow_html=True)

# --- PANTALLA: VISTA DE SOLICITUDES ---
elif st.session_state.page == 'LISTA':
    st.title("Lista de Solicitudes")
    if st.button("🏠 Home"): go_to('HOME')
    
    # Filtros simulados
    f1, f2, f3 = st.columns(3)
    f1.selectbox("PRODUCTO", ["Todos", "Tienda", "Micronegocios"])
    f2.selectbox("ESTADO", ["Pendiente", "En Proceso", "Finalizado"])
    f3.selectbox("CANAL", ["Todos", "Own", "Paid", "Real State"])

    # Datos simulados (como en tu imagen 5)
    data = {
        "ESTADO": ["PENDIENTE", "FINALIZADO", "EN PROCESO"],
        "PRODUCTO": ["MICRONEGOCIOS", "TIENDA", "TIENDA"],
        "FECHA": ["14 abril 2026", "14 abril 2026", "14 abril 2026"],
        "CANAL": ["TIK TOK", "PUSH", "PUSH"],
        "CAMPAÑA": ["PRUEBA", "audio", "televisores"]
    }
    df = pd.DataFrame(data)
    st.table(df) # En la web se puede hacer interactiva con st.dataframe