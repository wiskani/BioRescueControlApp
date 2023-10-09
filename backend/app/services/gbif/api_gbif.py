from pygbif import species
from typing import Optional

# Get species suggestions
def get_species_suggestions(query:str, r:Optional[str])->dict:
    if not r:
        return species.name_suggest(q=query)
    else:
        return species.name_suggest(q=query, rank=r)

# Get species details
def get_species_details(key:str)->dict:
    return species.name_usage(key=key, data='all')
