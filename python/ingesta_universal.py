import pandas as pd
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "consultor_universal.db"
DATA_DIR = BASE_DIR / "data"

def ejecutar_ingesta_total():
    # 1. Detectar cualquier CSV
    archivos = list(DATA_DIR.glob("*.csv"))
    if not archivos: return print("No hay archivos CSV.")
    
    ultimo_archivo = max(archivos, key=lambda p: p.stat().st_mtime)
    df = pd.read_csv(ultimo_archivo)
    
    # 2. Limpieza de nombres de columnas para SQL (quitar espacios y puntos)
    df.columns = [c.replace(' ', '_').replace('.', '_').strip() for c in df.columns]
    
    # 3. Guardar con nombre genérico
    conn = sqlite3.connect(DB_PATH)
    df.to_sql("datos_maestros", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Dataset '{ultimo_archivo.name}' cargado como 'datos_maestros'.")

if __name__ == "__main__":
    ejecutar_ingesta_total()