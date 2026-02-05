# Consultor Estratégico Universal (AI-Powered BI)

Este proyecto es una plataforma de Inteligencia de Negocios **agnóstica al dataset**. Utiliza IA Generativa para analizar cualquier archivo CSV, transformarlo en una base de datos relacional y generar diagnósticos ejecutivos automáticos.

## Características Útiles
* **Ingesta Automática:** Convierte cualquier CSV en SQL sin configurar nombres de columnas.
* **Dashboard Dinámico:** Se adapta automáticamente a las columnas numéricas y de texto detectadas.
* **Capa de IA:** Integración con Gemini para interpretación de contexto empresarial.
* **Reportes PDF:** Exportación de hallazgos y gráficas a un documento profesional.

## Instalación
1. Clona el repositorio.
2. Instala dependencias: `pip install -r requirements.txt`.
3. Coloca tu CSV en la carpeta `/data`.
4. Ejecuta la ingesta: `python python/ingesta_universal.py`.
5. Lanza la app: `streamlit run python/app.py`.# Motor-de-Consultor-a-Universal-con-IA
