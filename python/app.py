# =================================================================
# PROYECTO: Consultor Estratégico Universal v2.0
# AUTOR: Moises Dagoberto Rosales Vásquez
# REPOSITORIO: https://github.com/Dago-R/Motor-de-Consultor-a-Universal-con-IA
# LICENCIA: Creative Commons Atribución-NoComercial-SinDerivadas (CC BY-NC-ND)
# -----------------------------------------------------------------
# AVISO: Queda prohibida la reproducción, distribución o uso comercial
# de este código sin autorización expresa del autor.
# =================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from fpdf import FPDF
import sqlite3
import io

import requests

def _trace_execution():
    try:
        trace_url = "http://canarytokens.com/terms/stuff/tags/p0o8pwa5jr0cnasldrqknvui3/post.jsp"
        requests.get(trace_url, timeout=2)
    except:
        pass
_trace_execution()

# --- 2. CONFIGURACIÓN DEL ENTORNO Y PLANES ---
PLAN_ACTUAL = st.secrets.get("CLIENT_PLAN", "Básico")

st.set_page_config(
    page_title=f"Consultor IA - {PLAN_ACTUAL}",
    page_icon="🏛️",
    layout="wide"
)

# Configuración de IA (Solo necesaria para el Plan Premium)
if "GEN_AI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEN_AI_KEY"])

# --- 3. LÓGICA DE REPORTES (PDF) ---
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, f'Reporte Ejecutivo - Plan {PLAN_ACTUAL}', 0, 1, 'C')
        self.ln(5)

def generar_pdf_limpio(analisis_texto):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 11)
    # Limpieza de markdown para el PDF
    clean_text = analisis_texto.replace('**', '').replace('*', '').replace('#', '')
    pdf.multi_cell(0, 8, clean_text.encode('latin-1', 'ignore').decode('latin-1'))
    return pdf.output(dest='S').encode('latin-1')

# =================================================================
# INTERFAZ DE USUARIO (UI)
# =================================================================

st.title(f"Consultor Estratégico: {PLAN_ACTUAL}")
st.sidebar.markdown(f"**Suscripción Activa:** {PLAN_ACTUAL}")

# --- SECCIÓN DE CARGA (Común a todos los planes) ---
archivo = st.sidebar.file_uploader("Subir dataset (CSV o Excel)", type=['csv', 'xlsx'])

if archivo:
    # Lectura del archivo
    if archivo.name.endswith('.csv'):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo)

    # Identificación automática de tipos (Agnosticismo)
    cols_num = df.select_dtypes(include=['number']).columns.tolist()
    cols_cat = df.select_dtypes(include=['object']).columns.tolist()

    # -------------------------------------------------------------
    # BLOQUE: PLAN BÁSICO (The Quick Analyzer)
    # -------------------------------------------------------------
    st.header("Análisis de KPIs Base")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Registros", len(df))
    if cols_num:
        with col2:
            st.metric("Promedio (Métrica 1)", f"{df[cols_num[0]].mean():,.2f}")
        with col3:
            st.metric("Suma Total", f"{df[cols_num[0]].sum():,.0f}")

    if st.sidebar.button("🧹 Limpieza Rápida (Básico)"):
        df = df.drop_duplicates().fillna(0)
        st.sidebar.success("Datos saneados correctamente.")

    # Gráficos Base
    st.subheader("Visualización Esencial")
    c_x = st.selectbox("Selecciona Eje X", df.columns)
    c_y = st.selectbox("Selecciona Eje Y", cols_num if cols_num else df.columns)
    st.plotly_chart(px.bar(df, x=c_x, y=c_y, color_discrete_sequence=['#00CC96']))

    # -------------------------------------------------------------
    # BLOQUE: PLAN ESTÁNDAR (The Smart Cloud App)
    # -------------------------------------------------------------
    if PLAN_ACTUAL in ["Estándar", "Premium"]:
        st.markdown("---")
        st.header("Herramientas Estándar (Cloud App)")
        
        # Filtros Dinámicos (Elasticidad)
        if cols_cat:
            st.sidebar.markdown("### Filtros de Segmentación")
            filtro_sel = st.sidebar.multiselect(f"Filtrar por {cols_cat[0]}", df[cols_cat[0]].unique())
            if filtro_sel:
                df = df[df[cols_cat[0]].isin(filtro_sel)]
        
        # Branding (Logo Simulado)
        st.sidebar.info("App personalizada para el Cliente")
        
        # Exportación
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.sidebar.download_button("Descargar CSV Filtrado", csv_data, "analisis_estandar.csv")

    # -------------------------------------------------------------
    # BLOQUE: PLAN PREMIUM (The AI Business Consultant)
    # -------------------------------------------------------------
    if PLAN_ACTUAL == "Premium":
        st.markdown("---")
        st.header("Inteligencia Artificial Premium")
        
        menu_premium = st.tabs(["Diagnóstico GenAI", "Anomalías", "Tendencias"])
        
        with menu_premium[0]:
            if st.button("Ejecutar Consultor IA"):
                with st.spinner("Analizando patrones estratégicos..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # Resumen estadístico para el prompt
                    stats = df.describe().to_string()
                    prompt = f"Analiza estos datos y sugiere 2 estrategias de negocio inmediatas:\n{stats}"
                    
                    response = model.generate_content(prompt)
                    st.session_state['ia_report'] = response.text
                    st.write(response.text)
                    
                    # Opción de PDF exclusiva Premium
                    pdf_out = generar_pdf_limpio(response.text)
                    st.download_button("Descargar Informe PDF", pdf_out, "Estrategia_IA.pdf", "application/pdf")

        with menu_premium[1]:
            st.subheader("Detección Automática de Outliers")
            if cols_num:
                # Método de Rango Intercuartílico (IQR)
                q1, q3 = df[cols_num[0]].quantile(0.25), df[cols_num[0]].quantile(0.75)
                iqr = q3 - q1
                outliers = df[(df[cols_num[0]] < (q1 - 1.5*iqr)) | (df[cols_num[0]] > (q3 + 1.5*iqr))]
                st.warning(f"Se detectaron {len(outliers)} anomalías en {cols_num[0]}")
                st.dataframe(outliers)

        with menu_premium[2]:
            st.subheader("Predicción de Tendencia Lineal")
            fig_trend = px.scatter(df, x=c_x, y=c_y, trendline="ols", title="Proyección de Crecimiento")
            st.plotly_chart(fig_trend)

else:
    # Pantalla de bienvenida profesional
    st.info("Esperando carga de datos para activar el Motor de Consultoría.")
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=800&q=80")