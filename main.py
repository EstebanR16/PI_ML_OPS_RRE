from API_Transform import PlayTimeGenre, UserForGenre, UsersRecommend, UsersWorstDeveloper, Sentiment_analysis
from fastapi import FastAPI

app_recomendacion = FastAPI()

# Importacion de funciones: 

@app_recomendacion.get("/")
def read_root():
    return {"message": "¡Bienvenido a la API de Recomendaciones!"}

@app_recomendacion.get("/playtime-genre/{genero}")
def read_playtime_genre(genero: str):
    result = PlayTimeGenre(genero)
    return {"result": result}

@app_recomendacion.get("/user-for-genre/{genero}")
def read_user_for_genre(genero: str):
    result = UserForGenre(genero)
    return {"result": result}

@app_recomendacion.get("/users-recommend/{año}")
def read_users_recommend(año: int):
    result = UsersRecommend(año)
    return {"result": result}

@app_recomendacion.get("/users-worst-developer/{año}")
def read_users_worst_developer(año: int):
    result = UsersWorstDeveloper(año)
    return {"result": result}

@app_recomendacion.get("/sentiment-analysis/{empresa_desarrolladora}")
def read_sentiment_analysis(empresa_desarrolladora: str):
    result = Sentiment_analysis(empresa_desarrolladora)
    return {"result": result}
