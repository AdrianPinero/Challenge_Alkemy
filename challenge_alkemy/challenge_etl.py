import requests
import io
import pandas as pd
from datetime import datetime
import os
from config import lista_links
from sql_challenge import acceder_bbdd, actualizar_tablas
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


def extraer_csv(lista_links):
    """ Descarga y guarda los archivos .csv segun su tipo y fecha 

    ARGS:
        lista_links: lista de los links de donde descargará los archivos.

    Return:
        lista_rutas: devuelve una lista de rutas donde guardó la información.

    """
    logging.info("Extrayendo archivos csv.")
    lista_rutas = []

    for link in lista_links:
        try:
            response = requests.get(link)

            texto = response.text
            primer_split = texto.split(
                'class="btn btn-green btn-block" href="')
            segundo_split = primer_split[1].split('">DESCARGAR<')
            link_csv = segundo_split[0]  # Link del csv a descargar
            s = requests.get(link_csv).content
            df = pd.read_csv(io.StringIO(s.decode('utf-8')))

            a = texto.split('\n    Datos Argentina - ')
            b = a[1].split('</title>')
            categoria = b[0].lower()
            if categoria == 'museo':
                categoria = 'museos'

            fecha = datetime.now()  # Obteniendo la fecha al momento
            ano = fecha.year
            mes = fecha.month
            dia = fecha.day
            if dia < 10:
                dia = '0' + str(dia)

            meses = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
                     'julio', 'agosto', 'septiembre', 'octubre', 'noviembre',
                     'diciembre']
            mes_nombre = meses[mes-1]

            if mes < 10:
                mes = '0' + str(mes)

            ruta_carpeta = categoria + "/" + str(ano) + '-' + mes_nombre
            ruta_csv = categoria + "/" + str(ano) + '-' + mes_nombre + '/' + \
                categoria + '-' + str(dia) + '-' + str(mes) + \
                '-' + str(ano) + '.csv'

            os.makedirs(ruta_carpeta, exist_ok=True)
            df.to_csv(ruta_csv, index=False)
            lista_rutas.append(ruta_csv)
        except:
            logging.critical("No se pudo obtener los archivos .csv")

    return lista_rutas


def transformar(rutas):
    """ Transforma la informacion de museos, bibliotecas y salas de cine

    ARGS:
        rutas: lista de rutas de archivos .csv a trnasformar

    """
    logging.info("Transformando las tablas.")
    for ruta in rutas:

        df = pd.read_csv(ruta)

        # Cada uno de los archivos tiene ciertas características distintas
        if ruta.startswith('museos'):
            df.rename({
                'categoria': 'categoría',
                'Cod_Loc': 'cod_localidad',
                'IdProvincia': 'id_provincia',
                'IdDepartamento': 'id_departamento',
                'direccion': 'domicilio',
                'CP': 'código postal',
                'Mail': 'mail',
                'Web': 'web'}, axis=1, inplace=True)

            # Normalizo la data
            df['categoría'] = 'Museo'
            df['código postal'].fillna('s/d', inplace=True)
            df['domicilio'].fillna('s/d', inplace=True)
            df.replace('Neuquén\xa0', 'Neuquén', inplace=True)
            df['cod_area'] = df.cod_area.astype('Int64').astype('str')
            df['cod_area'].replace('<NA>', '', inplace=True)
            df['número de teléfono'] = df['cod_area'].astype(
                'str') + ' ' + df['telefono']
            df['número de teléfono'].fillna('s/d', inplace=True)
            df['mail'].fillna('s/d', inplace=True)
            df['web'].fillna('s/d', inplace=True)

            df.to_csv('museos/museos reciente.csv', index=False)

        else:

            df.rename({
                'Cod_Loc': 'cod_localidad',
                'IdProvincia': 'id_provincia',
                'IdDepartamento': 'id_departamento',
                'Provincia': 'provincia',
                'Categoría': 'categoría',
                'Localidad': 'localidad',
                'Nombre': 'nombre',
                'Domicilio': 'domicilio',
                'CP': 'código postal',
                'Mail': 'mail',
                'Web': 'web'
            }, axis=1, inplace=True)

            # Normalizo la data
            df.replace({
                'Tierra del Fuego':
                    'Tierra del Fuego, Antártida e Islas del Atlántico Sur',
                'Santa Fé': 'Santa Fe',
                'Neuquén\xa0': 'Neuquén'
            },
                inplace=True)
            df['web'].fillna('s/d', inplace=True)

            if ruta.startswith('salas de cine'):
                lista_tlf = []  # Creo una lista para agregar los telefonos
                for i in range(len(df)):
                    if df.cod_area[i] == 's/d':
                        lista_tlf.append('s/d')
                    else:
                        lista_tlf.append(
                            df.cod_area[i] + ' ' + df['Teléfono'][i])
                df['número de teléfono'] = pd.Series(lista_tlf)

                df.rename({'Pantallas': 'pantallas',
                           'Butacas': 'butacas',
                           'espacio_INCAA': 'espacio_incaa',
                           'Dirección': 'domicilio',
                           'Fuente': 'fuente'}, axis=1, inplace=True)

                # Sustituyo valores sin sentido
                df.butacas.replace(0, 's/d', inplace=True)
                df.butacas.fillna('s/d')
                df.espacio_incaa.replace({
                    'SI': 'si',
                    '0': 'no'},
                    inplace=True)
                df.espacio_incaa.fillna('no', inplace=True)

                df.to_csv(
                    'salas de cine/salas de cine reciente.csv', index=False)
            if ruta.startswith('bibliotecas populares'):

                lista_tlf = []
                for i in range(len(df)):
                    if df.Cod_tel[i] == 's/d':
                        lista_tlf.append('s/d')
                    else:
                        lista_tlf.append(
                            df.Cod_tel[i] + ' ' + df['Teléfono'][i])
                df['número de teléfono'] = pd.Series(lista_tlf)
                df.rename({'Fuente': 'fuente'}, axis=1, inplace=True)

                df.to_csv(
                    'bibliotecas populares/bibliotecas populares reciente.csv',
                    index=False)
    logging.info("Tablas transformadas")


def creacion_tablas():
    """Creacion de las tablas: unica, registros por categoria, fuente,
    provincia y categoria y la tabla cines

    """
    logging.info("Creando las tablas.")
    df1 = pd.read_csv(
        'bibliotecas populares/bibliotecas populares reciente.csv')
    df2 = pd.read_csv('museos/museos reciente.csv')
    df3 = pd.read_csv('salas de cine/salas de cine reciente.csv')

    tabla_col_completas = pd.concat([df1, df2, df3], ignore_index=True)
    lista = tabla_col_completas.fuente.tolist()

    for i in range(len(lista)):
        if pd.isna(lista[i]) or lista[i] == 's/d':
            tabla_col_completas.iloc[i] = pd.NA

    tabla_unica = pd.DataFrame(tabla_col_completas[[
        'cod_localidad',
        'id_provincia',
        'id_departamento',
        'categoría',
        'provincia',
        'localidad',
        'nombre',
        'domicilio',
        'código postal',
        'número de teléfono',
        'mail',
        'web'
    ]])

    registros_por_cat = pd.DataFrame(tabla_unica['categoría'].value_counts())
    registros_por_cat.columns = ['Registros por categoría']
    registros_por_cat.index.name = 'categoria'

    registros_por_fuente = pd.DataFrame(
        tabla_col_completas.fuente.value_counts())
    registros_por_fuente.columns = ['Registros por fuente']
    registros_por_fuente.index.name = 'fuente'

    registros_por_cat_prov = pd.DataFrame(
        tabla_unica[['provincia', 'categoría']].value_counts().sort_index())
    registros_por_cat_prov.columns = [
        'Registros']
    registros_por_cat_prov.index.name = 'categoria'

    tabla_cines = pd.DataFrame(
        df3[['provincia', 'pantallas', 'butacas', 'espacio_incaa']])

    tabla_cines.replace('s/d', 0, inplace=True)
    tabla_cines.replace('no', 0, inplace=True)
    tabla_cines.replace('si', 1, inplace=True)
    tabla_cines['butacas'] = tabla_cines['butacas'].astype('int64')

    cines_provincia = tabla_cines.groupby('provincia').sum()

    tabla_unica.to_csv('Tabla unica.csv', index=False)

    registros_por_cat.to_csv('Registros por categoria.csv', index=True)

    registros_por_fuente.to_csv('Registros por fuente.csv', index=True)

    registros_por_cat_prov.to_csv(
        'Registros por provincia y categoria.csv', index=True)

    cines_provincia.to_csv('Tabla cines.csv', index=True)
    logging.info("Tablas creadas.")


def etl():
    """ ETL. Corre las 3 funciones: extraer_csv, transformar y creacion_tablas

    """

    logging.info("Ejecutando ETL.")
    # Extraer
    rutas = extraer_csv(lista_links)

    # transform
    transformar(rutas)
    creacion_tablas()

    # load
    engine = acceder_bbdd()
    actualizar_tablas(engine)


if __name__ == '__main__':
    etl()
