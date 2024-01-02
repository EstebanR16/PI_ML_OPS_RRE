# PI_ML_OPS_RRE

***Desarrollo de sistema de recomendación (ML) y análisis mediante NLP en conjunto con el desarrollo de una API (Fast API + Render) para hacer poder levantar consultas en la web***

Steam es una plataforma multinacional de videojuegos, del cuaul necesitamos crear un sistema de recomendacion de videojuegos para usuarios.

### 1.- Ingesta de datos y Transformaciones
Se cargan todas (o la mayoria) de las librerias que vamos a utilziar a lo largo del desarrollo del programa, y ademas cargamos nuestros set de datos (que estan en formato JSON).

> [!Note]
> Necesitamos extraer previamente los archvios tipo **JSON** ya que vienen comprimidos en formato **gz**.

Por necesidades del cliente **no se requiere realizar transformaciones** ya que necesitamos consumir los datos tal y como se descargan de nuestra fuente (API).

### 2.- Feature Engineering

En el dataset user_reviews se incluyen reseñas de juegos hechos por distintos usuarios. Creamos la columna 'sentiment_analysis' aplicando análisis de sentimiento con _NLP_ con la siguiente escala: 

+ malo --> 0

+ neutral --> 1

+ bueno --> 2

+ Si el dato es Null --> 1

Para realziar el anális de sentiminento es necesaria la libreria **nltk**
```python
pip install nltk
```
> [!Tip]
> Esta libreria junto con todas las necesarias se cargan en el archivo **requirements.txt**
> Pero recordemos que se debe ejecutar el comando:
> ```python
>pip freeze > requirements.txt
> ```

## 3.- Desarrollo de API
Disponibilizamos los datos de la empresa usando el framework FastAPI + Render.
En donde podremos realizar diversas consultas, pero antes de eso debemos realziar algunos pasos para que sea mas eficiente y rápido el desarrollo de esta.

### Pasos:

### 3.1) Creamos el entorno virtual:

Pasos para poder correr la FastAPI:

+ Se recomienda instalar un entorno virtual en tu computador local.

--> python -m venv Nombre del entorno virtual

+ Se activa el entorno (API_Recomendacion)

--> nombre\Scripts\activate

+ Se instala FastAPI

--> pip install "fastapi[all]"

+ Nos dirigimos a la ruta de nuestro archivo main.py

+ llamamos a nuestro archivo de FastAPI

-->  uvicorn main:app --reload
    > uvicorn nombre_archvio:nombre de instancia (o tambien llamada aplicacion) --reload

### 3.2) Archivos necesarios del repositorio (GitHub)

+ Creacion de archivos
```
touch .gitignore
touch main.py
touch requirements.txt
```
> [!Note]
> El archivo main.py es el que contiene la lógica de nuestro sistema de recomendación (Nuesta **APP**)

### 3.3) Entorno virtual dentro de .gitignore

Vamos a poner el nombre del entorno virtual que creamos anteriormente en el archivo .gitignore:
```
/nombre_entorno/
```
> [!Tip]
> Se abre el archivo con cualquier editor de textos y guardar manualmente

### 3.4) Inizializar Git (consola Git bash)

La ruta en donde se crearon los archivos (en la consola de Git bash) es la misma que en donde esta el archivo ***main.py***
```
git init
pip install uvicorn
pip install fastapi
```

+ Descarga de librerias

```
pip freeze > requirements.txt
```
> [!Note]
> Se van a cargar todas las librerias que estan dentro de ***main.py*** y además siempre que utilicemos alguna nueva se tiene ejectuar nuevamente

### 3.5) Entorno virtual (cmd)

Si ya has creado tu entorno virtual, actívalo utilizando el comando correspondiente según tu sistema operativo.
```
API_Recomendacion\Scripts\activate
```

+ Instalar dependencias desde 'requirements.txt'
Una vez que el entorno virtual está activado, ejecuta el siguiente comando para instalar las dependencias listadas en requirements.txt:
```
pip install -r requirements.txt
```
Este comando instalará todas las librerías y versiones especificadas en requirements.txt dentro del entorno virtual activado.



  
> [!Warning]
> Estos es una nota

> [!Caution]
> Estos es una nota
