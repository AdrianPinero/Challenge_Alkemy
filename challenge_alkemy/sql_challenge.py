from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import pandas as pd
from datetime import datetime
from config import link_bbdd
import logging


def acceder_bbdd():
    """Conecta a la base de datos del archivo settings.ini (bbdd_link).

    Return:
        engine: resultante de la funcion create_engine(url)
    Se utiliza el engine para actualizar las tablas.

    """

    url_bbdd = link_bbdd

    if not database_exists(url_bbdd):
        create_database(url_bbdd)

    logging.info(f'conectando a la base de datos {url_bbdd}')
    try:
        engine = create_engine(url_bbdd, echo=False)
        return engine
    except:
        logging.critical('No se pudo acceder a la base de datos')


def actualizar_tablas(engine):
    """Actualiza las tablas de la base de datos a la cual esta conectada en
    el engine.

    ARGS:
        engine: generado con la funcion de sqlalchemy create_engine


    """
    # Leo todas las tablas creadas
    tabla_unica = pd.read_csv('Tabla unica.csv')
    registros_cat = pd.read_csv('Registros por categoria.csv')
    registros_fuente = pd.read_csv('Registros por fuente.csv')
    registros_prov_cat = pd.read_csv('Registros por provincia y categoria.csv')
    tabla_cines = pd.read_csv('Tabla cines.csv')

    # Creo la columna "fecha de carga"
    fecha = datetime.now()
    fecha_carga = str(fecha.year) + '-' + \
        str(fecha.month) + '-' + str(fecha.day)

    tabla_unica['fecha de carga'] = fecha_carga
    tabla_unica.to_sql('tabla_unica', engine, if_exists='replace', index=False)
    logging.info('Tabla unica actualizada.')

    registros_cat['fecha de carga'] = fecha_carga
    registros_cat.to_sql('registros_por_categoria', engine,
                         if_exists='replace', index=False)
    logging.info('Tabla registros por categoría actualizada.')

    registros_fuente['fecha de carga'] = fecha_carga
    registros_fuente.to_sql('registros_por_fuente',
                            engine, if_exists='replace', index=False)
    logging.info('Tabla registros por fuente actualizada.')

    registros_prov_cat['fecha de carga'] = fecha_carga
    registros_prov_cat.to_sql(
        'registros_por_prov_y_cat', engine, if_exists='replace', index=False)
    logging.info('Tabla registros por provincia y categoría actualizada.')

    tabla_cines['fecha de carga'] = fecha_carga
    tabla_cines.to_sql('tabla_cines', engine, if_exists='replace', index=False)
    logging.info('Tabla cines actualizada.')
