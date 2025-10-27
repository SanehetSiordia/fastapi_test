from fastapi import FastAPI

app = FastAPI()
#Modificacion de openapi FastApi
app.title ="HolaMundo fastAPI SSM"
app.version= "0.0.1-SNAPSHOT"

@app.get('/', tags=['Home'])
def home():
    return "Hola Mundo!!"