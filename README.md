# PI_ML_OPS_RRE

***Desarrollo de sistema de recomendación (ML) y análisis mediante NLP en conjunto con el desarrollo de una API (Fast API + Render) para hacer poder levantar consultas en la web***

Steam es una plataforma multinacional de videojuegos, del cuaul necesitamos crear un sistema de recomendacion de videojuegos para usuarios.

Fentes de informacion y documentacion: 

https://github.com/HX-FNegrete/render-fastapi-tutorial 

https://fastapi.tiangolo.com/

https://dashboard.render.com/web/new


## 1.- Ingesta de datos y Transformaciones
Se cargan todas (o la mayoria) de las librerias que vamos a utilziar a lo largo del desarrollo del programa, y ademas cargamos nuestros set de datos (que estan en formato JSON).

> [!Note]
> Necesitamos extraer previamente los archvios tipo **JSON** ya que vienen comprimidos en formato **gz**.

Por necesidades del cliente **no se requiere realizar transformaciones** ya que necesitamos consumir los datos tal y como se descargan de nuestra fuente (API).

## 2.- Feature Engineering

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

### 3.1) Creamos el entorno virtual (cmd):

Pasos para poder correr la FastAPI:

+ Se recomienda instalar un entorno virtual en tu computador local.

        python -m venv Nombre del entorno virtual

+ Se activa el entorno (API_Recomendacion)

        nombre\Scripts\activate

+ Para desactivar el entorno virtual

        deactivate 

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

### 3.4) Inizializar Git (desde terminal VSCode)

La ruta en donde se crearon los archivos (en la consola de Git bash) es la misma que en donde esta el archivo ***main.py***
```
git init
pip install uvicorn
pip install fastapi
```

> [!Note]
> Se van a cargar todas las librerias que estan dentro de ***main.py*** y además siempre que utilicemos alguna nueva se tiene ejectuar nuevamente

### 3.5) Entorno virtual (cmd)

Si ya has creado tu entorno virtual, actívalo utilizando el comando correspondiente según tu sistema operativo.

+ Nos dirigimos a la ruta de nuestro archivo main.py

        cd Desktop\.......

+ Vamos a activar nuestro entorno virtual (en el path  donde lo creamos)

  > En Windows:
  
    ```
    API_Ret\Scripts\activate
    ```
        
  > En sistemas basados en Unix:
  
  ```
    source API_Ret\bin\activate
  ``` 
+ Se instala FastAPI

        pip install "fastapi[all]"
        pip install (Todas las librerias que se ocupen)
> [!Tip]
> Aquí tambien vamos a poder cargar todas las paqueterias que sean necesarias para que funcione nuestro archivo **main.py**, con el comando:
>     ```pip install nombre_paqueteria```

+ Descarga de librerias

Una vez que ya están todas las librerías descargadas en nuestro entorno virtual, podemos hacer el freeze de los requirements, para generar un archivo requirements.txt basado en las bibliotecas instaladas actualmente en tu entorno virtual.

```
pip freeze > requirements.txt
```
>[!Warning]
>Instalar dependencias desde 'requirements.txt' (es para simular le mismo entorno)
>Una vez que el entorno virtual está activado, ejecuta el siguiente comando para instalar las dependencias listadas en requirements.txt:
> ```
>pip install -r requirements.txt
>```
> > Este comando instalará todas las librerías y versiones especificadas en **requirements.txt** dentro del entorno virtual activado.

+ llamamos a nuestro archivo de FastAPI

Inicializar el servidor de FasAPI.

      uvicorn main:app --reload
  
> uvicorn nombre_archvio:nombre de instancia (o tambien llamada aplicacion) --reload

> [!Note]
> Esta es la estructura general del archivo ***main.py***

```python
from fastapi import FastAPI
from API_Retencion import Clientes_por_Mes, Mes_mayorClientes, Mes_mayor_abandono, Porcentaje_Retencion_Abandono

app_retencion = FastAPI()

@app_retencion.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Recomendaciones!"}

@app_retencion.get("/clientes-mes/{mes}")
def obtener_clientes_por_mes(mes: str):
    result = Clientes_por_Mes(mes)
    return {"result": result}
```
> Tenemos un archivo llamado "API_Retencion.py" el cual contiene verdaderamente toda la lógica de nuestras funciones de consulta de la API


  
> [!Warning]
> Si al instalar ***requirements.txt*** se muestra alguna descarga incompleta es posible que se deba a una actualizacion del archivo ***main.py*** y deba descargar la paqueteria correspondiente.

### 3.6) Probar la API:
Una vez que la aplicación esté en ejecución, abre tu navegador y ve a:

http://127.0.0.1:8000/docs. 

Esto abrirá la interfaz de documentación interactiva de FastAPI (Swagger). Aquí puedes probar tus endpoints directamente desde el navegador.


## 4.- Git y Commit.

Después de realizar cambios, utiliza los siguientes comandos para agregar y confirmar tus cambios en Git:

        git add .
        git commit -m "Descripción de los cambios"
        
## 5.- GitHub

Asegúrate de que tu repositorio esté alojado en GitHub y de que hayas realizado el primer 'push':

        git remote add origin URL_DEL_REPO
        git branch -M main
        git push -u origin main
## 6.- Render

### 6.1) Configuración en Render:

Entrar en render.com y crearse una nueva cuenta de usuario.

Elegir la opción Web Service

Ir al apartado que se encuentra abajo de Public Git repository. 

Copiar y pegar el enlace del repositorio que crearon anteriormente (recuerden que sea público).

Accede a tu cuenta en Render y crea un nuevo servicio.

Configura el servicio para que apunte a tu repositorio de GitHub y especifique el archivo main.py como punto de entrada.

        pip install -r requirements.txt

### 6.2) Entorno Virtual en Render:

Asegúrate de que Render ejecute los comandos necesarios para activar tu entorno virtual y ejecutar tu aplicación. 

El resto de los campos se deben llenar con la misma información que en la imagen:

Esto podría ser algo así como:

        uvicorn main:app --host 0.0.0.0 --port 1000

Seleccionar la opción Create Web Service

## 7.- Despliegue

### 7.1) Despliegue en Render:

Realiza un despliegue manual desde la interfaz de Render o espera a que Render lo haga automáticamente cuando detecte cambios en tu repositorio.

### 7.2) Verificación:

Accede a la URL proporcionada por Render para verificar que tu aplicación FastAPI está funcionando correctamente en producción.

Nos va a direccionar a nuestra API. Si les aparece un "Not found", no se preocupen, agreguenle un /docs a su enlace.

