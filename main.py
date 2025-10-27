from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
#Modificacion de openapi FastApi
app.title ="HolaMundo fastAPI SSM"
app.version= "0.0.1-SNAPSHOT"

#Retorno Ejemplo de lista con diccionario
movies = [
    {
        "id":1,
        "title":"Avatar",
        "overview":"Pitufos Azules Extraterrestres por Christopher Nolan",
        "year":"2009",
        "raiting":8.5
    },
    {
        "id":2,
        "title":"Pitufos",
        "overview":"Pitufos Azules",
        "year":"1998",
        "raiting":5.5
    }
]

@app.get('/movies', tags=['Home'])
def get_movies():
    return movies


@app.get('/movies/{id}', tags=['Home'])
def get_movie(id: int):
    for movie in movies:
        if movie['id']==id:
            return movie
    return []