Challenge data Data Analytics - Python



	Requisitos básicos.

Python 3.10.4
Python es el lenguaje de programacion que se utilizo para crear los programas
que resuelven el challenge

Virtualenv
Virtual env es necesario para correr el entorno virtual donde se instalaran los
paquetes y se correran los programas. Si no lo tienes instalado, puedes
instalarlo desde cmd utilizando el comando "pip install virtualenv"

Paquetes
Creé un archivo requirements.txt donde estan los paquetes utilizados para poder
correr los programas. Estos paquetes se instalaran automaticamente como explico
mas adelante, igualmente puedes abrir el archivo si deseas revisarlo.



	Preparacion
Virtualenv
Teniendo instalado el paquete, se debe abrir la consola cmd, localizamos la
carpeta "challenge_alkemy". Una vez ubicados dentro de la carpeta dentro de
cmd, ejecutamos "python -m venv nombre" sustituyendo "nombre" por el nombre
de archivo que querramos. Para acceder al entorno virtual ejecutamos 
"nombre\Scripts\activate.bat"

Paquetes
Para instalar los paquetes dentro del entorno virtual, dentro del entorno
virtual, ejecutamos "pip install -r requirements.txt". Esto debe descargar e 
instalar todos los paquetes utilizados en los programas.

Base de datos
En el archivo settings.ini hay una variable "bbdd_link. Por favor, sustituye
su valor con la dirección correcta. Debes sustituir "usuario" por tu usuario
de postgresql, "contrasenha" por la contraseña, "host" por el host (Ej.
localhost), "puerto" por el puero (Ej. 5432), y la base de datos por el nombre
de la base de datos que quieras.

Las variables "link_museos", "link_bibliotecas" y "link_cines" tienen como 
valor el url más reciente al momento de enviar el archivo de sus respectivas
páginas. Si en algun momento cambian los url, modificar estas variables con 
los valores correctos. 

Tener en cuenta que el script que descarga el archivo .csv de la página, esta
hecho precisamente para el formato y codigo de la página. Si en algún momento
esto cambia, el script no podrá obtener el archivo .csv de la página.

	

	Ejecución

Para ejecutar la creacion de las tablas en sql hay que correr el archivo 
"script_tablas.py"

Para obtener los archivos .csv de museos, cines y bibliotecas, transformar la
data y guardarla dentro de las tablas creadas con "script_tablas.py" hay que
correr  "challenge_etl.py"
