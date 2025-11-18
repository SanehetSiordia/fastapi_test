import os
from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.exceptions import HTTPException
from typing import Annotated
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler
from jose import jwt

app = FastAPI()
#Modificacion de openapi FastApi
app.title ="HolaMundo fastAPI SSM"
app.version= "0.0.1-SNAPSHOT"

#OAuth2Password Esquema
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

#Importar middleware para manejo de errores con Starlette
app.middleware(HTTPErrorHandler) 

#Rutas para estilos y templates de plantillas html
static_path = os.path.join(os.path.dirname(__file__), 'static/')
templates_path = os.path.join(os.path.dirname(__file__), 'templates/')

#Carga de archivos de ruta espeficia
app.mount('/static', StaticFiles(directory=static_path),'static')
templates= Jinja2Templates(directory=templates_path)

#Diccionario de ejemplo para usuarios y datos.
users={
    "Sinhue":{"username":"Sinhue","email":"sinhue@gmail.com","password":"9871231"},
    "UsuarioX":{"username":"UsuarioX","email":"userx@gmail.com","password":"userX"},
}

#Funcionas Encoder y Decoder para Tokens Generados
#Con JWT se suministra:
# 1.-El diccionario con los datos para armar el token (payload).
# 2. Una clave secreta (GUARDAR EN VARIABLES DE ENTORNO)
# 3. El algoritmo para generar token
def encode_token(payload: dict) -> str:
    token = jwt.encode(payload,"my-secret",algorithm="HS256")
    return token

#El token se debe pasar en los Headers de la Ruta y no por tipo QUERY
#Por lo que se usa Annotated
def decode_token(token: Annotated[str,Depends(oauth2_schema)]) -> dict:
    data=jwt.decode(token, "my-secret",algorithms=["HS256"])
    user=users.get(data["username"])
    return user

#Url login con token
@app.post("/token")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user=users.get(form_data.username)
    if not user or form_data.password!=user["password"]:
        raise HTTPException(status_code=400, detail="Incorrect Username or Password")
    token=encode_token({"username":user["username"],"email":user["email"]})
    return {"access_token":token}

#Ruta para obtener la informacion del usuario a la que pertenece el Token Generado.
@app.get("/user/profile")
def profile(my_user:Annotated[dict,Depends(decode_token)]):
    return my_user

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
