from pygbif import species
from typing import Optional, Dict
from fastapi import HTTPException

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
    # check if data is SpecieGbif
    try :
        data = SpecieGbif(**data)
        return data
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


# Get species details
def get_species_details_test(key:str)-> Dict:
    data = species.name_usage(key=key, data='all')
    return data
