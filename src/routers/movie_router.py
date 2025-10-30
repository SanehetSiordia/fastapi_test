from fastapi import Path, Query, APIRouter
from fastapi.responses import JSONResponse, RedirectResponse
from typing import List

from src.models.movie_models import Movie, MovieCreate, MovieUpdate

#Retorno Ejemplo de lista DE OBJETOS TIPO Movie
movies : List[Movie] = []

#Routers para llamar los metodos en FASTAPI
movie_router = APIRouter()

@movie_router.get('/', tags=['Movies'],status_code=200)
def get_movies()->List[Movie]:
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content, status_code=200)
    
#PATH PARAM
@movie_router.get('/{id}', tags=['Movies'],status_code=200)
def read_movie(id: int = Path(gt=0))->Movie | dict:
    for movie in movies:
        if movie.id==id:
            return JSONResponse(content=movie.model_dump(),status_code=200)
    return JSONResponse(content={},status_code=404)

#QUERY PARAM
@movie_router.get('/category', tags=['Movies'],status_code=200)
def get_movie_by_category(category: str = Query(min_length=5, max_length=20))->Movie | dict:
    for movie in movies:
        if movie.category==category:
            return JSONResponse(content=movie.model_dump(),status_code=200)
    return  JSONResponse(content={},status_code=404)

#POST METHOD
@movie_router.post('/', tags=['Movies'],status_code=303, response_description='Redireccion Exitosa')
def create_movie(movie:MovieCreate)->List[Movie]:
    movies.append(movie) #Se registra solo el objeto
    content = [movie.model_dump() for movie in movies]
    #return JSONResponse(content=content)
    return RedirectResponse('/movies', status_code=303)

#PUT METHOD
@movie_router.put('/{id}', tags=['Movies'],status_code=201, response_description='Modificacion Exitosa')
def update_movie(id: int,movie:MovieUpdate)->List[Movie]:
    for item in movies:
        if item.id==id:
            item.title=movie.title
            item.overview=movie.overview
            item.year=movie.year
            item.raiting=movie.raiting
            item.category=movie.category
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=201)

#DELETE METHOD
@movie_router.delete('/{id}', tags=['Movies'],status_code=200, response_description='Eliminacion Exitosa')
def delete_movie(id:int)->List[Movie] | dict:
    for movie in movies:
        if movie.id==id:
            movies.remove(movie)
    content = [movie.model_dump() for movie in movies]
    return JSONResponse(content=content,status_code=200)