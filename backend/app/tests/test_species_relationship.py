from typing import Dict, Any
from sqlalchemy.orm import Session


from app.tests.conftest import *
from app.models.species import Specie, Genus
from app.tests.utils.species_example import  *


#test for relationship between species and genus
#def test_relation_with_genus()-> None:
#
#    #create a genus
#    response = client.post(
#        "/api/genuses/", json={
#            "genus_name": "test_genus name",
#            "genus_full_name": "test_genus common name",
#            "family_id": create_family_id(),
#        },
#    )
#    assert response.status_code == 201, response.text
#    data: Dict[str, Any] = response.json()
#    genus: int = data["id"]
#
#    #create a species 1
#    response = client.post(
#        "/api/species/", json={
#            "scientific_name": "test_species name 1",
#            "specific_epithet": "test_species common name 1",
#            "genus_id": genus,
#        },
#    )
#    assert response.status_code == 201, response.text
#
#    #create a species 2
#    response = client.post(
#        "/api/species/", json={
#            "scientific_name": "test_species name 2",
#            "specific_epithet": "test_species common name 2",
#            "genus_id": genus,
#        },
#    )
#    assert response.status_code == 201, response.text
#
#    #create a species 3
#    response = client.post(
#        "/api/species/", json={
#            "scientific_name": "test_species name 3",
#            "specific_epithet": "test_species common name 3",
#            "genus_id": 10011,
#        },
#    )
#    # Make a query to the database
#    species = db.query(Specie).join(Genus, Specie.genus_id == Genus.id).filter(Specie.genus_id == genus).all()
#
#    # Create a list of dictionaries with the data
#    species_data = [
#            {
#                "scientific_name": s.scientific_name,
#                "specific_epithet": s.specific_epithet,
#                "genus_id": s.genus_id
#                }
#            for s in species
#            ]
#
#    # Create a list of dictionaries with the expected data
#    expected_data = [
#            {
#                "scientific_name": "test_species name 1",
#                "specific_epithet": "test_species common name 1",
#                "genus_id": genus
#                },
#            {
#                "scientific_name": "test_species name 2",
#                "specific_epithet": "test_species common name 2",
#                "genus_id": genus
#                }
#            ]
#
#    # Compare the data
#    assert species_data == expected_data
#
#
#
#
