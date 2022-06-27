from pathlib import Path


ruta_archivo = Path().resolve()

ruta_sql = Path(ruta_archivo, "sql")

lista_tablas = [
    'tabla_unica',
    'registros_por_categoria',
    'registros_por_fuente',
    'registros_por_prov_y_cat',
    'tabla_cines'
]
