from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import datetime

app = FastAPI()
#Modificacion de openapi FastApi
app.title ="HolaMundo fastAPI SSM"
app.version= "0.0.1-SNAPSHOT"

#Clase de modelo con pydantic para catalogo
class Movie (BaseModel):
    id: int
    title:str
    overview:str
    year:int
    raiting:float
    category:str

#Clase de modelo con pydantic para registrar datos con validaciones
class MovieCreate (BaseModel):
    id: int
    title:str = Field(min_length=5,max_length=15, default='my movie')
    overview:str = Field(min_length=10,max_length=50)
    year:int = Field(ge=1850,le=datetime.date.today().year)
    raiting:float = Field(le=10,ge=0)
    category:str = Field(min_length=5,max_length=10)

    #Configuracion de tipo de objeto
    model_config={
        'json_schema_extra':{
            'example':{
                'id':1,
                'title':'my movie',
                'overview':'This movie is about...',
                'year':1950,
                'raiting':5.0,
                'category':'Comedy'
            }
        }
    }

class MovieUpdate (BaseModel):
    title:str
    overview:str
    year:int
    raiting:float
    category:str

#Retorno Ejemplo de lista DE OBJETOS TIPO Movie
movies : List[Movie] = []

@app.get('/movies', tags=['Home'])
def get_movies()->List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)
    
#PATH PARAM
@app.get('/movies/{id}', tags=['Movies'])
def read_movie(id: int = Path(gt=0))->Movie | dict:
    for movie in movies:
        if movie.id==id:
            return JSONResponse(content=movie.model_dump())
    return JSONResponse(content={})

#QUERY PARAM
@app.get('/movies/', tags=['Movies'])
def get_movie_by_category(category: str = Query(min_length=5, max_length=20))->Movie | dict:
    for movie in movies:
        if movie.category==category:
            return JSONResponse(content=movie.model_dump())
    return  JSONResponse(content={})

#POST METHOD
@app.post('/movies', tags=['Movies'])
def create_movie(movie:MovieCreate)->List[Movie]:
    movies.append(movie) #Se registra solo el objeto
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)

#PUT METHOD
@app.put('/movies/{id}', tags=['Movies'])
def update_movie(id: int,movie:MovieUpdate)->List[Movie]:
    for item in movies:
        if item.id==id:
            item.title=movie.title
            item.overview=movie.overview
            item.year=movie.year
            item.raiting=movie.raiting
            item.category=movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)

#DELETE METHOD
@app.delete('/movies/{id}', tags=['Movies'])
def delete_movie(id:int)->List[Movie] | dict:
    for movie in movies:
        if movie.id==id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content)