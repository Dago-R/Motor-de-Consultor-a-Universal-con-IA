# Consultor Estratégico Universal: Engine de BI & GenAI Agnostic

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-orange.svg)](https://ai.google.dev/)
[![SQLite](https://img.shields.io/badge/SQLite-3.0-green.svg)](https://www.sqlite.org/)

Este proyecto es una plataforma de **Analítica Prescriptiva** diseñada para transformar datos crudos en decisiones estratégicas sin intervención manual. A diferencia de los sistemas de BI tradicionales, este motor es **agnóstico al esquema**, lo que permite procesar cualquier dataset (ventas, inventarios, logística, RRHH) de forma automática.

---

## El Problema: Rigidez en el Análisis de Datos
En el flujo convencional de análisis, los desarrolladores y analistas enfrentan:
* **Esquemas Rígidos:** Los scripts fallan si los nombres de las columnas cambian o si el dataset proviene de una fuente distinta.
* **Dashboards Mudos:** Las gráficas muestran *qué* ocurrió, pero carecen de la interpretación profesional para explicar el *por qué*.
* **Fricción de Ingesta:** El proceso de limpiar CSVs y cargarlos a una base de datos suele ser manual y propenso a errores.

## La Solución: Arquitectura Universal y Adaptativa
Este sistema implementa una arquitectura de tres capas para garantizar flexibilidad total:

### 1. Ingesta Universal (Data Engineering)
El componente `ingesta_universal.py` actúa como una capa de abstracción:
* **Normalización Dinámica:** Escanea la carpeta `/data`, detecta el CSV más reciente y sanitiza los nombres de las columnas para SQL automáticamente.
* **Motor SQL:** Convierte datos planos en una base de datos relacional SQLite funcional en segundos.

### 2. Dashboard Interactivo (Visualización)
Desarrollado en `Streamlit`, la interfaz no depende de variables fijas:
* **Interrogación del Esquema:** Detecta automáticamente qué columnas son métricas (números) y cuáles son dimensiones (texto).
* **Explorador Multidimensional:** Permite al usuario cruzar cualquier variable del dataset de forma dinámica.

### 3. Consultoría GenAI (Inteligencia Artificial)
Integración nativa con **Gemini 1.5 Flash** para actuar como un economista senior:
* **Deducción de Contexto:** La IA analiza el esquema y una muestra de los datos para inferir el giro de negocio.
* **Diagnóstico Profesional:** Genera un análisis crítico sobre tendencias, anomalías y riesgos estratégicos.

---

## Guía de Instalación

### 1. Requisitos Previos
* Python 3.9 o superior.
* Una API Key de [Google AI Studio](https://aistudio.google.com/).

### 2. Instalación
```bash
# Clonar el repositorio
git clone [https://github.com/Dago-R/Motor-de-Consultor-a-Universal-con-IA.git)
cd Motor-de-Consultor-a-Universal-con-IA

# Instalar dependencias
pip install -r requirements.txt
