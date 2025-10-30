#Clase de modelo con pydantic para catalogo
from pydantic import BaseModel, Field, field_validator
import datetime


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
    title:str = Field(default='my movie')
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
    @field_validator('title')
    @classmethod
    def validate_title(cls,value):
        if len(value) < 5:
            raise ValueError('Title field must have more than 4 characteres')
        elif len(value) > 15:
            raise ValueError('Title field must have minus than 16 characters')
        return value

class MovieUpdate (BaseModel):
    title:str
    overview:str
    year:int
    raiting:float
    category:str