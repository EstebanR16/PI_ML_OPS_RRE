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

### Pasos

### 3.1) Creamos el entorno virtual:

Pasos para poder correr la FastAPI:

+ Se recomienda instalar un entorno virtual en tu computador local.
--> python -m venv Nombre del entorno virtual

+ Se activa el entorno (API_Recomendacion)
--> nombre\Scripts\activate

+ Se instala FastAPI
--> pip install "fastapi[all]"

+ Nos dirigimos a la ruta de nuestro archivo main.py

+ llamammos a nuestro archivo de FastAPI7
-->  uvicorn main:app --reload
  > [!Tip]
  > uvicorn nombre_archvio:nombre de instancia (o tambien llamada aplicacion) --reload


> [!Warning]
> Estos es una nota

> [!Caution]
> Estos es una nota
