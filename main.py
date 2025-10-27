from fastapi import FastAPI, Body
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
        "raiting":8.5,
        "category":"action"
    },
    {
        "id":2,
        "title":"Pitufos",
        "overview":"Pitufos Azules",
        "year":"1998",
        "raiting":5.5,
        "category":"family"
    }
]

@app.get('/movies', tags=['Home'])
def get_movies():
    return movies

#PATH PARAM
@app.get('/movies/{id}', tags=['Movies'])
def read_movie(id: int):
    for movie in movies:
        if movie['id']==id:
            return movie
    return []

#QUERY PARAM
@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str, year: int):
    for movie in movies:
        if movie['category']==category:
            return movie
    return []

#POST METHOD
@app.post('/movies', tags=['Movies'])
def create_movie(
    id:int=Body(),
    title:str=Body(),
    overview:str=Body(),
    year:str=Body(),
    raiting:float=Body(),
    category:str=Body()
    ):

    movies.append({
        'id':id,
        'title':title,
        'overview':overview,
        'year':year,
        'raiting':raiting,
        'category':category
    })
    return movies

#PUT METHOD
@app.put('/movies/{id}', tags=['Movies'])
def update_movie(
    id:int,
    title:str=Body(),
    overview:str=Body(),
    year:str=Body(),
    raiting:float=Body(),
    category:str=Body()
    ):
    for movie in movies:
        if movie['id']==id:
            movie['title']=title
            movie['overview']=overview
            movie['year']=year
            movie['raiting']=raiting
            movie['category']=category
    return movies

#DELETE METHOD
@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int):

    for movie in movies:
        if movie['id']==id:
            movies.remove(movie)
    return movies