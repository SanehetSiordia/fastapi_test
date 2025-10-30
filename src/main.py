from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from src.routers.movie_router import movie_router

app = FastAPI()
#Modificacion de openapi FastApi
app.title ="HolaMundo fastAPI SSM"
app.version= "0.0.1-SNAPSHOT"

@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content='Home')

#Creacion de las rutas en MAIN
app.include_router(prefix='/movies', router=movie_router)
