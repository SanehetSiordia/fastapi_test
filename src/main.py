import os
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler

app = FastAPI()
#Modificacion de openapi FastApi
app.title ="HolaMundo fastAPI SSM"
app.version= "0.0.1-SNAPSHOT"

#Importar middleware para manejo de errores con Starlette
app.middleware(HTTPErrorHandler) 

#Rutas para estilos y templates de plantillas html
static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

#Carga de archivos de ruta espeficia
app.mount('/static', StaticFiles(directory=static_path),'static')
templates= Jinja2Templates(directory=templates_path)

@app.get('/', tags=['Home'])
def home(request:Request):
    #Renderizado al iniciar
    return templates.TemplateResponse('index.html',{'request':request,'message':'Welcome'})

#Creacion de las rutas en MAIN
app.include_router(prefix='/movies', router=movie_router)
