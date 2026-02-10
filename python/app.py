import streamlit as st
import pandas as pd
import plotly.express as px
import google.generativeai as genai
from fpdf import FPDF
import sqlite3
import io

# 1. CONFIGURACIÓN DE SEGURIDAD Y API
st.set_page_config(page_title="Consultor Universal IA", layout="wide")

# Intentar cargar la API Key desde los Secretos de Streamlit
if "GEN_AI_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEN_AI_KEY"])
else:
    st.warning("⚠️ API Key no detectada. Configura 'GEN_AI_KEY' en los Secrets de Streamlit para usar funciones Premium.")

# 2. LÓGICA DE PDF (LIMPIEZA DE MARKDOWN)
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Reporte de Consultoria Estrategica IA', 0, 1, 'C')
        self.ln(5)

def generar_pdf(df, analisis_ia):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Diagnostico Ejecutivo', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    # Limpieza de caracteres Markdown para evitar errores en FPDF
    texto_limpio = analisis_ia.replace('**', '').replace('*', '').replace('#', '').replace('---', '')
    texto_limpio = texto_limpio.encode('latin-1', 'ignore').decode('latin-1')
    
    pdf.multi_cell(0, 8, texto_limpio)
    return pdf.output(dest='S').encode('latin-1')

# 3. SIDEBAR: CARGA DE ARCHIVOS Y PLANES
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=100)
st.sidebar.title("Panel de Control")

# Selector de Plan (Lógica de Bloqueo)
plan = st.sidebar.selectbox("Selecciona tu Plan", ["Básico", "Estándar", "Premium"])

st.sidebar.markdown("---")
archivo_subido = st.sidebar.file_uploader("Sube tu dataset (CSV o Excel)", type=['csv', 'xlsx'])

if archivo_subido:
    # Lectura dinámica
    if archivo_subido.name.endswith('.csv'):
        df = pd.read_csv(archivo_subido)
    else:
        df = pd.read_excel(archivo_subido)

    # Ingesta SQL en Memoria (Demostración de manejo de SQL)
    conn = sqlite3.connect(':memory:', check_same_thread=False)
    # Sanitizar nombres de columnas para SQL
    df_sql = df.copy()
    df_sql.columns = [c.replace(' ', '_').replace('.', '').replace('(', '').replace(')', '') for c in df_sql.columns]
    df_sql.to_sql("datos_maestros", conn, index=False)

    # 4. INTERFAZ PRINCIPAL
    st.title(f"Consultor Universal - Plan {plan}")
    
    # --- PAQUETE BÁSICO ---
    st.header("1. KPIs Principales")
    cols_num = df.select_dtypes(include=['number']).columns
    
    if not cols_num.empty:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Registros Totales", len(df))
        with col2:
            st.metric("Suma Métrica Principal", f"{df[cols_num[0]].sum():,.0f}")
        with col3:
            st.metric("Promedio", f"{df[cols_num[0]].mean():,.2f}")
    
    # --- PAQUETE ESTÁNDAR ---
    if plan in ["Estándar", "Premium"]:
        st.markdown("---")
        st.header("2. Explorador Dinámico (Business Intelligence)")
        
        col_dim, col_met = st.columns(2)
        with col_dim:
            dimension = st.selectbox("Dimensión (Texto)", df.select_dtypes(include=['object']).columns)
        with col_met:
            metrica = st.selectbox("Métrica (Número)", cols_num)
        
        # Consulta SQL para el gráfico
        query = f"SELECT {dimension.replace(' ', '_')}, SUM({metrica.replace(' ', '_')}) as Total FROM datos_maestros GROUP BY 1 ORDER BY Total DESC LIMIT 10"
        df_plot = pd.read_sql(query, conn)
        
        fig = px.bar(df_plot, x=df_plot.columns[0], y='Total', title=f"Top 10 {dimension} por {metrica}", color='Total')
        st.plotly_chart(fig, use_container_width=True)

    # --- PAQUETE PREMIUM ---
    if plan == "Premium":
        st.markdown("---")
        st.header("3. Consultoría Estratégica con IA")
        
        if st.button("Generar Diagnóstico Ejecutivo"):
            with st.spinner("Gemini está analizando la base de datos SQL..."):
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Contexto dinámico para la IA
                resumen_datos = df.describe().to_string()
                prompt = f"""
                Actúa como un Consultor Senior de Estrategia. Analiza este resumen de datos:
                {resumen_datos}
                
                Instrucciones:
                1. Identifica el giro de negocio.
                2. Menciona 3 hallazgos clave.
                3. Da 2 recomendaciones accionables.
                Responde con un tono ejecutivo y profesional.
                """
                
                response = model.generate_content(prompt)
                st.session_state['analisis_ia'] = response.text
                st.markdown(response.text)
        
        if 'analisis_ia' in st.session_state:
            pdf_bytes = generar_pdf(df, st.session_state['analisis_ia'])
            st.download_button(
                label="Descargar Reporte PDF",
                data=pdf_bytes,
                file_name="Consultoria_IA.pdf",
                mime="application/pdf"
            )

else:
    st.info("Bienvenido. Por favor, sube un archivo CSV o Excel en la barra lateral para comenzar.")