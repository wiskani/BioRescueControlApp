from pygbif import species
from typing import Optional, Dict
from fastapi import HTTPException
from pydantic import ValidationError

from app.schemas.services import SpecieGbif

# Get species suggestions
def get_species_suggestions(query:str, r:Optional[str])->dict:
    if not r:
        return species.name_suggest(q=query)
    else:
        return species.name_suggest(q=query, rank=r)

# Get species details
def get_species_details(key:str)-> SpecieGbif| HTTPException:
    data = species.name_usage(key=key, data='all')
    #Chek if class is a reptilia
    if data['class'] == "Testudines" or data['class'] == "Squamata" or data['class'] == "Crocodilia" or data['class'] == "Sphenodontia":
        raise HTTPException(status_code=404, detail='Class Reptilia does not can be registered in the system automatically')
    # check if data is SpecieGbif
    try :
        data = SpecieGbif(**data)
        return data
    except ValidationError as e:
        error_message = e.errors()
        raise HTTPException(status_code=404, detail=error_message)
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)

