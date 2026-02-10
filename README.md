# Consultor Estratégico Universal: Engine de BI & GenAI Agnostic

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-red.svg)](https://streamlit.io/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-2.5%20Flash-orange.svg)](https://ai.google.dev/)
[![License: Propia](https://img.shields.io/badge/License-Proprietary-red.svg)](LICENSE)

Este proyecto es una plataforma de **Analítica Prescriptiva** diseñada para transformar datos crudos en decisiones estratégicas sin intervención manual. A diferencia de los sistemas de BI tradicionales, este motor es **agnóstico al esquema**, lo que permite procesar cualquier dataset (ventas, inventarios, logística, RRHH) de forma automática.

---

Este motor de **Business Intelligence con IA** ha evolucionado de un script local a una solución **SaaS (Software as a Service)** escalable. Diseñado para empresas que necesitan diagnósticos ejecutivos instantáneos sin configuraciones técnicas.

## Nuevas Capacidades (v2.0)
* **Ingesta Cloud-Native:** Eliminación de dependencia de archivos locales. Carga de archivos vía interfaz web.
* **Motor SQL In-Memory:** Los datos se procesan en la memoria RAM del servidor mediante SQLite, garantizando velocidad y privacidad (nada se guarda en disco).
* **Niveles de Servicio (Tiers):** Implementación de lógica de negocios para planes Básico, Estándar y Premium.
* **Reportes Ejecutivos:** Generación de PDFs profesionales libres de formatos Markdown, listos para imprimir.

## Tecnologías Utilizadas
* **Core:** Python 3.9+
* **Engine de IA:** Google Gemini 2.5 Flash (Generative AI).
* **Base de Datos:** SQLite (SQL queries para análisis dinámico).
* **Visualización:** Plotly Express & Streamlit.
* **Infraestructura:** Streamlit Cloud & GitHub.

## Estructura de Oferta
1.  **Plan Básico:** Dashboard de KPIs generales y estadísticas descriptivas.
2.  **Plan Estándar:** Explorador de datos dinámico con filtros multidimensionales y gráficos SQL.
3.  **Plan Premium:** Consultoría completa con IA, diagnóstico narrativo y descarga de reportes PDF.

---

## Licencia y Propiedad Intelectual
Este software es de **Código Abierto para Inspección (Open-Source for Inspection)** pero de **Uso Restringido**. 
* **Copyright © 2026 Dagoberto Rosales**. 
* No se permite la reproducción, distribución o uso comercial del código sin autorización expresa. 
* Para licencias comerciales o despliegues personalizados, contactar a: https://www.linkedin.com/in/dagoberto-rosales/.

---

## Protocolos de Seguridad y Auditoría

Este software ha sido desarrollado bajo estándares de seguridad proactiva y control de integridad. Se han implementado los siguientes protocolos para proteger la propiedad intelectual del autor:

* **Auditoría de Despliegue (Canary Tokens):** El código fuente integra "objetos de seguimiento" que notifican al autor sobre cualquier ejecución en servidores no autorizados o réplicas del repositorio.
* **Monitoreo de IP y Hosting:** Cada ejecución del sistema registra la huella digital del entorno de hosting. Si se detecta un uso comercial fuera de la infraestructura oficial sin licencia, se activará un reporte automático de infracción de Copyright.
* **Protección de Lógica de Negocio:** Las funciones críticas de IA están protegidas mediante variables de entorno (Secrets). El acceso al motor de Gemini 2.5 Flash está restringido exclusivamente a la instancia oficial controlada por el autor.
* **Firma Digital de Código:** Cada versión estable cuenta con una marca de agua interna que identifica la procedencia del código fuente, permitiendo rastrear filtraciones o copias no autorizadas.

> **Advertencia:** Cualquier intento de ingeniería inversa, redistribución o despliegue paralelo sin el consentimiento por escrito de **Dagobeeto Rosales** será sujeto a las acciones legales correspondientes bajo las leyes de propiedad intelectual internacionales.
