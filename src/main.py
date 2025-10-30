from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse, PlainTextResponse
from src.routers.movie_router import movie_router
from src.utils.http_error_handler import HTTPErrorHandler

app = FastAPI()
#Modificacion de openapi FastApi
app.title ="HolaMundo fastAPI SSM"
app.version= "0.0.1-SNAPSHOT"

#Importar middleware para manejo de errores
#app.middleware(HTTPErrorHandler) #Starlette
@app.middleware('http')
async def http_error_handler(request:Request, call_next) -> Response | JSONResponse:
    print('Middleware is running!')
    try:
        return await call_next(request)    
    except Exception as e:
        content = f"ex: {str(e)}"
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return JSONResponse(content=content, status_code=status_code)

@app.get('/', tags=['Home'])
def home():
    return PlainTextResponse(content='Home')

#Creacion de las rutas en MAIN
app.include_router(prefix='/movies', router=movie_router)
