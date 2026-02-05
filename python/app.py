import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from pathlib import Path
import google.generativeai as genai
from fpdf import FPDF

# 1. Configuración de Rutas y Página
st.set_page_config(page_title="Consultor Estratégico IA", layout="wide")

BASE_DIR = Path(__file__).resolve().parent.parent
# Sincronizamos con el nombre que usa tu ingesta_universal.py
DB_PATH = BASE_DIR / "database" / "consultor_universal.db"

# 2. Configuración Gemini (Corregido a versión estable)
GEN_AI_KEY = "TU_API_KEY" 
genai.configure(api_key=GEN_AI_KEY)
model = genai.GenerativeModel('MODELO_IA_QUE_MEJOR_FUNCIONE')

# 3. Clase PDF Necesaria
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte de Consultoria Inteligente', 0, 1, 'C')
        self.ln(10)
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Pagina {self.page_no()}', 0, 0, 'C')

# 4. Funciones de Soporte
def cargar_dinamico():
    if not DB_PATH.exists():
        st.error(f"Base de datos no encontrada en: {DB_PATH}")
        st.stop()
    conn = sqlite3.connect(str(DB_PATH)) 
    try:
        # Cargamos la tabla genérica creada por la ingesta
        df = pd.read_sql("SELECT * FROM datos_maestros", conn)
    finally:
        conn.close()
    return df

def generar_pdf_universal(df, analisis_ia):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '1. Muestra de Datos Analizados', 0, 1)
    pdf.ln(5)
    
    cols_pdf = df.columns[:5].tolist()
    pdf.set_font('Arial', 'B', 10)
    col_width = 190 / len(cols_pdf)
    for col in cols_pdf:
        pdf.cell(col_width, 10, str(col)[:15], 1, 0, 'C')
    pdf.ln()
    
    pdf.set_font('Arial', '', 9)
    for _, row in df.head(10).iterrows():
        for col in cols_pdf:
            pdf.cell(col_width, 10, str(row[col])[:20], 1)
        pdf.ln()
    
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, '2. Diagnostico Estrategico', 0, 1)
    pdf.set_font('Arial', '', 11)
    
    texto_limpio = analisis_ia.encode('ascii', 'ignore').decode('ascii')
    pdf.multi_cell(0, 8, texto_limpio)
    return pdf.output(dest='S')

# --- LÓGICA DE INTERFAZ ---
st.title("Consultor Estratégico Universal")

try:
    df = cargar_dinamico()
    col_numericas = df.select_dtypes(include=['number']).columns.tolist()
    col_texto = df.select_dtypes(include=['object']).columns.tolist()

    # Sidebar
    st.sidebar.header("Explorador Dinamico")
    eje_x = st.sidebar.selectbox("Agrupar por:", options=col_texto if col_texto else df.columns)
    eje_y = st.sidebar.selectbox("Metrica a evaluar:", options=col_numericas if col_numericas else df.columns)
    
    # KPIs
    st.markdown("### Indicadores Clave")
    k_cols = st.columns(min(len(col_numericas), 4))
    for i, c_met in enumerate(col_numericas[:4]):
        k_cols[i].metric(c_met.replace('_', ' ').title(), f"{df[c_met].mean():,.2f}")

    # Gráfico
    st.markdown("---")
    fig = px.bar(df.groupby(eje_x)[eje_y].sum().reset_index(), x=eje_x, y=eje_y, 
                 title=f"Distribucion de {eje_y} por {eje_x}", template="plotly_dark", color=eje_y)
    st.plotly_chart(fig, use_container_width=True)

    # IA
    if st.button("Generar Diagnostico con IA"):
        with st.spinner("Analizando tendencias..."):
            esquema = df.dtypes.to_string()
            muestra = df.head(15).to_string()
            prompt = f"Analiza estos datos como consultor senior. Esquema: {esquema}. Datos: {muestra}. Deduce el contexto y da 3 recomendaciones."
            
            response = model.generate_content(prompt)
            st.session_state['analisis_ia'] = response.text
            st.markdown("### Diagnostico de la IA")
            st.write(response.text)

    # Botón PDF
    if 'analisis_ia' in st.session_state:
        pdf_bytes = generar_pdf_universal(df, st.session_state['analisis_ia'])
        st.download_button("Descargar Reporte PDF", data=bytes(pdf_bytes), file_name="consultoria.pdf", mime="application/pdf")

except Exception as e:
    st.error(f"Error en el motor: {e}")