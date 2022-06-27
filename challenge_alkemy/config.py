from decouple import AutoConfig
from constantes import ruta_archivo

config = AutoConfig(search_path=ruta_archivo)

link_bbdd = config("bbdd_link")

link_museos = config("link_museos")
link_cines = config("link_cines")
link_bibliotecas = config("link_bibliotecas")

lista_links = [
    link_museos,
    link_cines,
    link_bibliotecas
]
