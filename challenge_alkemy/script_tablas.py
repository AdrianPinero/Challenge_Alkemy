from constantes import lista_tablas, ruta_sql
from sql_challenge import acceder_bbdd
import logging

log = logging.getLogger()
log.setLevel(logging.INFO)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
if len(log.handlers) < 1:
    log.addHandler(ch)


def crear_tablas():
    """Creando las tablas en la base de datos"""
    engine = acceder_bbdd()
    for tabla in lista_tablas:
        log.info(f'Creando la tabla: {tabla}')
        with open(ruta_sql / f"{tabla}.sql", 'r') as archivo:
            data = archivo.read()

        engine.connect().execute(f"DROP TABLE IF EXISTS {tabla}")
        engine.connect().execute(data)


if __name__ == '__main__':
    crear_tablas()
