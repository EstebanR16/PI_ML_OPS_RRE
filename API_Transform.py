import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import json
import ast

# Se extrajeron anteriormente (ya sea manual o en python)
archivo_json1 = 'output_steam_games.json' 
archivo_json2 = 'australian_users_items.json'
archivo_json3 = 'australian_user_reviews.json'

def carga_archivo_json(archivo_json):
    # Inicializa una lista para almacenar los diccionarios de cada archivo
    data = []

    # Lee cada línea del archivo y carga los objetos JSON en la lista
    with open(archivo_json, 'r', encoding='utf-8') as f:
        for linea in f:
            try:
                # Utiliza json.loads para cargar el objeto JSON de la línea actual
                obj_json = json.loads(linea)
                
                # Agrega el objeto a la lista
                data.append(obj_json)
            except json.JSONDecodeError as e:
                # Si hay un error, intenta evaluar la línea con ast.literal_eval
                try:
                    # Utiliza ast.literal_eval para parsear la línea
                    parsed_line = ast.literal_eval(linea)
                    
                    # Convierte el resultado a JSON
                    json_line = json.dumps(parsed_line)
                    
                    # Carga el objeto JSON de la línea actual
                    obj_json = json.loads(json_line)
                    
                    # Agrega el objeto a la lista
                    data.append(obj_json)
                except (SyntaxError, json.JSONDecodeError) as e:
                    # Si hay un error, agrega un diccionario vacío
                    data.append({})

    # Retorna la lista de diccionarios al finalizar la función
    return data

datos_steam= carga_archivo_json(archivo_json1)
datos_items= carga_archivo_json(archivo_json2)
datos_reviews= carga_archivo_json(archivo_json3)


# Crea un DataFrame a partir de la lista de diccionarios
df_steam = pd.DataFrame(datos_steam)
df_items = pd.DataFrame(datos_items)
df_reviews = pd.DataFrame(datos_reviews)

# Cargamos toda libreria necesaria
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.sentiment import SentimentIntensityAnalyzer

# Descarga recursos necesarios de NLTK
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('vader_lexicon')

                    #### Análisis de sentimientos ####
                    
# Preprocesamiento del Texto
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

#funcion para procesar el texto
def preprocess_text(review_list):
    processed_reviews = []
    for review_dict in review_list:
        text = review_dict.get('review', '')  # Obtiene el valor asociado con la clave 'review', si existe
        words = word_tokenize(text) #crea cada uno de los token con repecto a cada review
        words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words] 
        words = [lemmatizer.lemmatize(word) for word in words]
        processed_reviews.append(' '.join(words))
    return processed_reviews

# Aplica preprocesamiento del texto a la columna 'reviews'
df_reviews['processed_reviews'] = df_reviews['reviews'].apply(preprocess_text)

# Análisis de Sentimientos
sia = SentimentIntensityAnalyzer()

# Aplica análisis de sentimientos a cada revisión y toma el compuesto como el sentimiento
df_reviews['sentiment'] = df_reviews['processed_reviews'].apply(lambda reviews: [sia.polarity_scores(review)['compound'] for review in reviews])

# Puedes promediar los sentimientos de todas las revisiones para obtener un sentimiento general por fila
df_reviews['average_sentiment'] = df_reviews['sentiment'].apply(lambda sentiments: sum(sentiments) / len(sentiments) if sentiments else 0)

def categorize_sentiment(sentiment):
    if sentiment >= 0.05:
        return 2  # Bueno
    elif sentiment <= -0.05:
        return 0  # Malo
    else:
        return 1  # Medio

# Aplica la función a la columna 'average_sentiment' para obtener las etiquetas
df_reviews['sentiment_analysis'] = df_reviews['average_sentiment'].apply(categorize_sentiment)


#Extraemos los valores que se encuentran en el diccionario de la fila df_items['items']
# para asi generar las columnas df_items['item_id'] y df_items['playtime_forever']

df_items['playtime_forever'] = df_items['items'].apply(lambda x: [item.get('playtime_forever', None) for item in x] if isinstance(x, list) else None)

        
df_items['item_id'] = df_items['items'].apply(lambda x: [item.get('item_id', None) for item in x] if isinstance(x, list) else None)

# Aplica una función lambda a la columna 'reviews', extrae la columna item_id
df_reviews['item_id'] = df_reviews['reviews'].apply(lambda reviews_list: [item.get('item_id', None) for item in reviews_list] if isinstance(reviews_list, list) else None)

# Pasamos a formato fecha la columna df_steam['release_year']
df_steam['release_date']=pd.to_datetime(df_steam['release_date'].str.strip(), format='%Y-%m-%d', errors='coerce')
#con errors=coerce, cuando encuentra un tipo de dato que no es datatime lo maneja como nulo


######### Extraemos todos lo generos  y tambien lo que se encuentran en tags

from typing import Union, Set, List, Any

# Convierte las listas de 'genres' y 'tags' a conjuntos para facilitar la comparación
df_steam['genres'] = df_steam['genres'].apply(lambda x: set(x) if isinstance(x, list) else x)
df_steam['tags'] = df_steam['tags'].apply(lambda x: set(x) if isinstance(x, list) else x)

# Obtiene los géneros únicos para la comparación
unique_genres = set(genre for genres_set in df_steam['genres'].dropna() for genre in genres_set)

# Define la función replace_genres dentro de UserForGenre
def replace_genres(row: Any, unique_genres: Set[str]) -> Union[Set[str], List[str]]:
    genres = row['genres']
    tags = row['tags']

    # Verifica si 'genres' no es un conjunto
    if not isinstance(genres, set):
        # Verifica si 'tags' es un conjunto
        if isinstance(tags, set):
            matching_genres = {tag for tag in tags if tag in unique_genres}
            if matching_genres:
                return matching_genres

    return genres

# Aplica la función a cada fila del DataFrame
df_steam['genres'] = df_steam.apply(lambda row: replace_genres(row, unique_genres), axis=1)

# Convierte todas las listas a conjuntos para evitar problemas de comparación
df_steam['genres'] = df_steam['genres'].apply(lambda x: set(x) if isinstance(x, list) else x)

def PlayTimeGenre(genero: str):
    genre = genero.capitalize()

    # Filtra el DataFrame por el género especificado
    df_filtered = df_steam[df_steam['genres'].apply(lambda x: genre in x if isinstance(x, set) else False)]

    if not df_filtered.empty:
        # Convierte las horas de juego solo si no hay valores None
        df_items['playtime_forever'] = df_items['playtime_forever'].apply(
            lambda x: [int(i / 60) if i is not None else None for i in x] if isinstance(x, list) else None
        )

        # Explota las listas en 'playtime_forever'
        df_items_id_exploded = df_items.explode('item_id')
        # Realizar la fusión (merge) utilizando las columnas 'id' y 'item_id'
        df_subset = pd.merge(df_filtered, df_items_id_exploded, left_on='id', right_on='item_id', how='inner')

        # Elimina las filas con listas vacías o valores nulos en 'playtime_forever'
        df_subset_cleaned = df_subset.dropna(subset=['playtime_forever']).reset_index(drop=True)

        if not df_subset_cleaned.empty:
            # Encuentra el índice del máximo
            max_playtime_index = df_subset_cleaned['playtime_forever'].apply(lambda x: max(x) if x else None).idxmax()

            # Verifica si el índice es válido antes de continuar
            if pd.notna(max_playtime_index):
                year_with_most_playtime = pd.to_datetime(df_subset_cleaned.loc[max_playtime_index, 'release_date']).year

                # Formatea el resultado
                result = {
                    "Año de lanzamiento con más horas jugadas para Género {}:".format(genre): year_with_most_playtime
                }
            else:
                result = {
                    "Año de lanzamiento con más horas jugadas para Género {}:".format(genre): "No hay datos válidos con horas jugadas"
                }
        else:
            result = {
                "Año de lanzamiento con más horas jugadas para Género {}:".format(genre): "No se encontraron datos con horas jugadas"
            }
    else:
        result = {
            "Año de lanzamiento con más horas jugadas para Género {}:".format(genre): "Género no encontrado"
        }

    return result
 
#Debe devolver año con mas horas jugadas para dicho género.
#Ejemplo de retorno: {"Año de lanzamiento con más horas jugadas para Género X" : 2013}

def UserForGenre(genero: str):
    genre = genero.capitalize()
    
    # Filtra el DataFrame por el género especificado
    df_filtered = df_steam[df_steam['genres'].apply(lambda x: genre in x if isinstance(x, set) else False)]

    if not df_filtered.empty:
        # Convierte las horas de juego solo si no hay valores None
        df_items['playtime_forever'] = df_items['playtime_forever'].apply(
            lambda x: [int(i / 60) if i is not None else None for i in x] if isinstance(x, list) else None
        )

    # Explota las listas en 'playtime_forever'
    df_items_id_exploded = df_items.explode('item_id')
    # Realizar la fusión (merge) utilizando las columnas 'id' y 'item_id'
    df_merged = pd.merge(df_filtered, df_items_id_exploded, left_on='id', right_on='item_id', how='inner')

    columnas_de_interes = ['user_id', 'playtime_forever', 'id','release_date','genres']
    df_subset = df_merged[columnas_de_interes]

    # Elimina las filas con listas vacías o valores nulos en 'playtime_forever'
    df_subset_cleaned = df_subset.dropna(subset=['playtime_forever']).reset_index(drop=True)

    # Verifica si el DataFrame filtrado no está vacío
    if not df_filtered.empty:
        # Inicializa variables para almacenar el máximo
        max_playtime = 0
        user_with_most_playtime = None
        max_playtime_by_year = {}

        # Itera sobre las filas del DataFrame filtrado
        for index, row in df_subset_cleaned.iterrows():
            # Comprueba si la lista 'playtime_forever' no está vacía
            if row['playtime_forever']:
                # Encuentra el máximo
                horas_jugadas = max(row['playtime_forever'])
                
                # Compara con el máximo actual
                if horas_jugadas > max_playtime:
                    max_playtime = horas_jugadas
                    user_with_most_playtime = row['user_id']

                # Agrega las horas jugadas por año a max_playtime_by_year
                release_year = pd.to_datetime(row['release_date']).year
                if release_year not in max_playtime_by_year:
                    max_playtime_by_year[release_year] = horas_jugadas
                else:
                    max_playtime_by_year[release_year] += horas_jugadas

        # Ordena las horas jugadas por año de mayor a menor
        sorted_hours_by_year = sorted(max_playtime_by_year.items(), key=lambda x: x[1], reverse=True)

        # Formatea el resultado
        result = {
            "Usuario con más horas jugadas para Género {}:".format(genre): user_with_most_playtime,
            "Horas jugadas": [{"Año": year, "Horas": hours} for year, hours in sorted_hours_by_year]
        }
        
    else:
        result = {
            "Usuario con más horas jugadas para Género {}:".format(genre): "Género no encontrado",
            "Horas jugadas": []
        }

    return result

"""
Debe devolver el usuario que acumula más horas jugadas para el género dado y una lista de la acumulación de horas jugadas por año.
Ejemplo de retorno: {"Usuario con más horas jugadas para Género X" : us213ndjss09sdf, "Horas jugadas":[{Año: 2013, Horas: 203}, {Año: 2012, Horas: 100}, {Año: 2011, Horas: 23}]}
"""
# 2 --> Positivo
# 1 --> Neutro
# 0 --> Negativo
def UsersRecommend(año: int):
    # Asumiendo que 'release_date' es una columna de tipo datetime en tu DataFrame
    df_steam['release_year'] = df_steam['release_date'].dt.year.astype('Int64')

    # Filtra el DataFrame para obtener solo las filas del año específico
    df_filtered_by_year = df_steam[df_steam['release_year'] == año]

    # Suponiendo que 'df_reviews['reviews']' contiene listas de diccionarios para poder extraer recommend
    df_reviews['recommend'] = df_reviews['reviews'].apply(lambda reviews: [review.get('recommend', False) for review in reviews])

    # Calcula el promedio de valores booleanos en cada lista y asigna el resultado a una nueva columna 'recommend_avg'
    df_reviews['recommend_avg'] = df_reviews['recommend'].apply(lambda x: np.mean(x) > 0.5 if x else np.nan)

    if not df_filtered_by_year.empty and not df_reviews.empty:

        # Filtra los reviews para aquellos con recomendación y comentarios positivos/neutrales
        df_reviews_filtered = df_reviews[df_reviews['recommend_avg'] & df_reviews['sentiment_analysis'].isin([2, 1])]
        #Ex necesario explotar la lista item_id 
        df_reviews_filtered_exploded = df_reviews_filtered.explode('item_id')

        # Realiza la fusión (merge) utilizando las columnas 'id' y 'item_id'
        df_merged = pd.merge(df_filtered_by_year, df_reviews_filtered_exploded, left_on='id', right_on='item_id', how='inner')

        columnas_de_interes = ['user_id', 'recommend_avg', 'id','title','release_year','genres']
        df_merged = df_merged[columnas_de_interes]

        #Agrupa por juego y cuenta las recomendaciones
        game_recommendations = df_merged.groupby('title')['recommend_avg'].sum()

        # Obtiene el top 3 de juegos más recomendados
        game_recommendations_filled = game_recommendations.fillna(0)

        # Obtiene el top 3 de juegos más recomendados
        top_3_recommendations = game_recommendations_filled.sort_values(ascending=False).head(3)

        # Formatea el resultado
        result = [{"Puesto {}: {}".format(i + 1, game): recommendations} for i, (game, recommendations) in enumerate(top_3_recommendations.items())]

    else:
        print("No pasa")
        result = [{"Puesto {}: ".format(i + 1): "No se encontraron datos"} for i in range(3)]


    return result
   
"""Devuelve el top 3 de juegos MÁS recomendados por usuarios para el año dado. (reviews.recommend = True y comentarios positivos/neutrales)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]"""

def UsersWorstDeveloper(año: int):
    # Asumiendo que 'release_date' es una columna de tipo datetime en tu DataFrame
    df_steam['release_year'] = df_steam['release_date'].dt.year.astype('Int64')

    # Filtra el DataFrame para obtener solo las filas del año específico
    df_filtered_by_year = df_steam[df_steam['release_year'] == año]

    # Suponiendo que 'df_reviews['reviews']' contiene listas de diccionarios para poder extraer recommend
    df_reviews['recommend'] = df_reviews['reviews'].apply(lambda reviews: [review.get('recommend', False) for review in reviews])

    # Calcula el promedio de valores booleanos en cada lista y asigna el resultado a una nueva columna 'recommend_avg'
    df_reviews['recommend_avg'] = df_reviews['recommend'].apply(lambda x: np.mean(x) > 0.5 if x else np.nan)

    if not df_filtered_by_year.empty and not df_reviews.empty:
        # Filtra los reviews para aquellos con NO recomendación y comentarios negativos [0]
        df_reviews_filtered = df_reviews[df_reviews['recommend_avg'] & df_reviews['sentiment_analysis'].isin([0])]

        # Explora la lista 'item_id' ya que es necesario para el merge
        df_reviews_filtered_exploded = df_reviews_filtered.explode('item_id')

        # Realiza la fusión (merge) utilizando las columnas 'id' y 'item_id'
        df_merged = pd.merge(df_filtered_by_year, df_reviews_filtered_exploded, left_on='id', right_on='item_id', how='inner')

        # Agrupa por desarrolladora y cuenta las NO recomendaciones
        developer_worst_recommendations = df_merged.groupby('developer')['recommend_avg'].sum()

        # Convierte la columna a tipo numérico
        developer_worst_recommendations = developer_worst_recommendations.astype(float)

        # Ordena en orden ascendente y obtén el top 3 (menos recomendados)
        bottom_3_developers = developer_worst_recommendations.sort_values().head(3)

        # Formatea el resultado
        result = [{"Puesto {}: {}".format(i + 1, developer): recommendations} for i, (developer, recommendations) in enumerate(bottom_3_developers.items())]

    else:
        result = [{"Puesto {}: ".format(i + 1): "No se encontraron datos"} for i in range(3)]

    return result

"""Devuelve el top 3 de desarrolladoras con juegos MENOS recomendados por usuarios para el año dado. (reviews.recommend = False y comentarios negativos)
Ejemplo de retorno: [{"Puesto 1" : X}, {"Puesto 2" : Y},{"Puesto 3" : Z}]"""

def Sentiment_analysis(empresa_desarrolladora: str):
    # Filtra el DataFrame para obtener las reseñas de la empresa desarrolladora
    df_steam_dev = df_steam[df_steam['developer'] == empresa_desarrolladora]

    # Explora la lista 'item_id' ya que es necesario para el merge
    df_reviews_exploded = df_reviews.explode('item_id')

    # Realiza la fusión (merge) utilizando las columnas 'id' y 'item_id'
    df_merged_SA = pd.merge(df_steam_dev, df_reviews_exploded, left_on='id', right_on='item_id', how='inner')

    columnas_de_interes = ['user_id', 'sentiment', 'sentiment_analysis', 'developer']
    df_merged_SA = df_merged_SA[columnas_de_interes]

    if not df_merged_SA.empty:
        # Realiza el análisis de sentimiento para las reseñas de la empresa
        sentiment_counts = df_merged_SA['sentiment_analysis'].value_counts()

        # Formatea el resultado
        result = {empresa_desarrolladora: {"Negative": sentiment_counts.get(0, 0),
                                           "Neutral": sentiment_counts.get(1, 0),
                                           "Positive": sentiment_counts.get(2, 0)}}

    else:
        result = {empresa_desarrolladora: {"Negative": 0, "Neutral": 0, "Positive": 0}}

    return result


#Según la empresa desarrolladora, se devuelve un diccionario con el nombre de la desarrolladora como llave y una lista con la cantidad total de registros de reseñas de usuarios que se encuentren categorizados con un análisis de sentimiento como valor.
#Ejemplo de retorno: {'Valve' : [Negative = 182, Neutral = 120, Positive = 278]}