import sqlite3
import pandas as pd
from pathlib import Path

# Configuración de rutas relativas profesionales
BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "features.csv"
DB_PATH = BASE_DIR / "database" / "features.db"

def procesar_datos_limpios():
    df_raw = pd.read_csv(CSV_PATH)
    # Corrección de errores de tipeo detectados
    df_raw['proveedor'] = df_raw['proveedor'].replace('Proveedo_A', 'Proveedor_A')
    
    conn = sqlite3.connect(DB_PATH)
    df_raw.to_sql("inventario_ventas", conn, if_exists="replace", index=False)
    conn.close()
    print("Base de datos actualizada con éxito.")

if __name__ == "__main__":
    procesar_datos_limpios()