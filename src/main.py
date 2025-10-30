import os
from fastapi import FastAPI, Request, Depends, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
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

#Inyeccion de dependencias
def commons_param(start_date:str, end_date:str):
    return {"start_date":start_date,"end_date":end_date}

commonsDep=Annotated[dict, Depends(commons_param)]

@app.get('/users', tags=['venta'])
def get_users(commons: commonsDep):    #dependencia declarada con Annotated de typing
    return f"Users created between {commons['start_date']} and {commons['end_date']}"

@app.get('/customers', tags=['venta'])
def get_customers(commons: dict=Depends(commons_param)):    #dependencia guardada como variable diccionario
    return f"Customers created between {commons['start_date']} and {commons['end_date']}"

#Creacion de las rutas en MAIN
app.include_router(prefix='/movies', router=movie_router)
