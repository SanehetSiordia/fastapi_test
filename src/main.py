import os
from fastapi import FastAPI, Request, Depends
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
#Tipo 1 con metodo y libreria FastApi - Depends
def commons_param(start_date:str, end_date:str):
    return {"start_date":start_date,"end_date":end_date}

#Tipo 2 con Annotated de Typing
commons_dependency=Annotated[dict, Depends(commons_param)]

#Tipo 3 con Clase
class CommonDependency:
    def __init__(self,start_date: str, end_date: str) -> None:
        self.start_date = start_date
        self.end_date = end_date

@app.get('/users', tags=['venta'])
def get_users(commons: commons_dependency):    #dependencia declarada con Annotated de typing
    return f"Users created between {commons['start_date']} and {commons['end_date']}"

@app.get('/customers', tags=['venta'])
def get_customers(commons: dict=Depends(commons_param)):    #dependencia guardada como variable diccionario
    return f"Customers created between {commons['start_date']} and {commons['end_date']}"


@app.get('/employees', tags=['venta'])
def get_users(commons: CommonDependency=Depends()):    #dependencia declarada con una clase (mismo nombre de variable igualada, se puede eliminar)
    return f"Employee created between {commons.start_date} and {commons.end_date}"


#Creacion de las rutas en MAIN
app.include_router(prefix='/movies', router=movie_router)
