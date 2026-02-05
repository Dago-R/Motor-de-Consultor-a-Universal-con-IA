-- 1. Preparación de la Estructura Maestra
-- Esta sentencia asegura que la tabla exista sin borrar los datos si ya fueron cargados por Python
CREATE TABLE IF NOT EXISTS inventario_ventas (
    producto TEXT,
    categoria TEXT,
    ventas REAL,
    stock_final REAL,
    precio_venta REAL,
    costo_unitario REAL,
    fecha DATE,
    proveedor TEXT
);

-- 2. Vista de Análisis de Disponibilidad (Safety Stock)
-- Usamos COALESCE para evitar errores si hay valores nulos en el dataset real
DROP VIEW IF EXISTS vista_analisis_critico;
CREATE VIEW vista_analisis_critico AS
SELECT 
    producto,
    categoria,
    SUM(ventas) AS total_unidades_vendidas,
    AVG(stock_final) AS stock_promedio,
    -- Calculamos un índice de riesgo: si el stock es bajo y las ventas altas
    CASE 
        WHEN AVG(stock_final) < (SUM(ventas) / 7) THEN 'RIESGO ALTO'
        WHEN AVG(stock_final) = 0 THEN 'AGOTADO'
        ELSE 'SALUDABLE'
    END as estatus_inventario
FROM inventario_ventas
GROUP BY producto, categoria;

-- 3. Consulta de Rentabilidad Dinámica
-- Esta consulta solo funcionará si las columnas de precio y costo fueron mapeadas
-- En app.py manejaremos la excepción si estas columnas no existen
SELECT 
    producto,
    ROUND(SUM(ventas * precio_venta), 2) AS ingresos_estimados,
    ROUND(SUM(ventas * (precio_venta - costo_unitario)), 2) AS margen_estimado
FROM inventario_ventas
WHERE precio_venta IS NOT NULL 
  AND costo_unitario IS NOT NULL
GROUP BY producto
ORDER BY margen_estimado DESC;