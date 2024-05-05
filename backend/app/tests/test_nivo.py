from httpx import Response, AsyncClient
from typing import Dict, Any, Union, List
import pytest

from app.tests.conftest import *
from app.tests.utils.species_example import *
from app.tests.utils.rescue_mammals import *
from app.tests.utils.rescue_herpetofauna import *
from app.tests.utils.flora_rescue_example import *

from app.schemas.nivo import (
        SunburstBase
        )


from app.services.nivo.sunburst import (
        create_sunburst_base_children,
        create_sunburst_data,
        )

from app.services.nivo.utils import (
        get_flora_families_rescues,
        get_herpetofauna_families_rescues,
        get_mammals_families_rescues,
        get_flora_families_relocation,
        get_herpetofauna_families_relocation,
        get_mammals_families_relocation,
        )


# test for create_sunburst_base_children
def test_create_sunburst_base_children() -> None:

    # Create list of names
    names: List[str] = [
            'Mammals',
            'Herpetofauna',
            'Birds',
            'Invertebrates',
            'Mammals',
            'Mammals',
            'Mammals',
            ]

    name = 'Mammals'

    color = "hsl(0, 100%, 50%)"

    # Create base children

    base_children = create_sunburst_base_children(
            name=name,
            children=names,
            color=color
            )

    # Expected result
    expected_result = SunburstBase(
            name='Mammals',
            color="hsl(0, 100%, 50%)",
            loc=4,
            children=None
            )

    assert base_children == expected_result


# test for get_flora_families
@pytest.mark.asyncio
async def test_get_flora_families_rescue(
        async_client: AsyncClient,
        async_session: AsyncSession
        ) -> None:

    # Create families
    specie1, genus1, family1, specieId1, genusId1, familyId1 = await create_specieWithFamily(async_client)
    specie2, genus2, family2, specieId2, genusId2, familyId2 = await create_specieWithFamily(async_client)
    specie3, genus3, family3, specieId3, genusId3, familyId3 = await create_specieWithFamily(async_client)

    RESCUE_ZONE_ID = await create_random_rescue_zone_id(async_client)

    # create flora rescue

    response = await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": "1",
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": "1.0",
            "rescue_area_longitude": "1.0",
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "is_epiphyte_confirmed": True,
            "is_bryophyte_confirmed": True,
            "specie_bryophyte_id": specieId1,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": None,
            "specie_epiphyte_id": specieId1,
            "genus_epiphyte_id": None,
            "family_epiphyte_id": None,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )

    assert response.status_code == 201

    response = await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": "2",
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": "1.0",
            "rescue_area_longitude": "1.0",
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "is_epiphyte_confirmed": True,
            "is_bryophyte_confirmed": True,
            "specie_bryophyte_id": None,
            "genus_bryophyte_id": genusId2,
            "family_bryophyte_id": None,
            "specie_epiphyte_id": None,
            "genus_epiphyte_id": genusId2,
            "family_epiphyte_id": None,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )
    assert response.status_code == 201

    response = await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": "3",
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": "1.0",
            "rescue_area_longitude": "1.0",
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "is_epiphyte_confirmed": True,
            "is_bryophyte_confirmed": True,
            "specie_bryophyte_id": None,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": familyId3,
            "specie_epiphyte_id": None,
            "genus_epiphyte_id": None,
            "family_epiphyte_id": familyId3,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )
    assert response.status_code == 201

    # Get flora families
    flora_families = await get_flora_families_rescues(async_session)

    # Expected result
    expected_result = [family1, family2, family3]

    assert flora_families == expected_result


# test for get_herpetofauna_families_rescues
@pytest.mark.asyncio
async def test_get_herpetofauna_families_rescues(
        async_client: AsyncClient,
        async_session: AsyncSession
        ) -> None:

    # Create families
    specie1, genus1, family1, specieId1, genusId1, familyId1 = await create_specieWithFamily(async_client)
    specie2, genus2, family2, specieId2, genusId2, familyId2 = await create_specieWithFamily(async_client)
    specie3, genus3, family3, specieId3, genusId3, familyId3 = await create_specieWithFamily(async_client)

    transect_herpetofauna_id: int = await create_transect_herpetofauna(async_client)
    age_group_id: int = await create_age_group(async_client)

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": "1",
            "gender": True,
            "specie_id": specieId1,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": "2",
            "gender": True,
            "specie_id": specieId2,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201

    response: Response = await async_client.post(
        "/api/rescue_herpetofauna", json={
            "number": "3",
            "gender": True,
            "specie_id": specieId3,
            "transect_herpetofauna_id": transect_herpetofauna_id,
            "age_group_id": age_group_id,
        },
    )
    assert response.status_code == 201

    # Get herpetofauna families
    herpetofauna_families = await get_herpetofauna_families_rescues(
            async_session
            )

    # Expected result
    expected_result = [family1, family2, family3]

    # Check result
    assert herpetofauna_families == expected_result


# test for get mammals_families
@pytest.mark.asyncio
async def test_get_mammals_families(
        async_client: AsyncClient,
        async_session: AsyncSession
        ) -> None:

    # Create families
    specie1, genus1, family1, specieId1, genusId1, familyId1 = await create_specieWithFamily(async_client)
    specie2, genus2, family2, specieId2, genusId2, familyId2 = await create_specieWithFamily(async_client)
    specie3, genus3, family3, specieId3, genusId3, familyId3 = await create_specieWithFamily(async_client)

    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": "1",
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": specieId1,
            "genus_id": None
        },
    )
    assert response.status_code == 201

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": "2",
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": specieId2,
            "genus_id": None
        },
    )
    assert response.status_code == 201

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": "3",
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": None,
            "genus_id": genusId3
        },
    )
    assert response.status_code == 201

    # Get mammals families
    mammals_families = await get_mammals_families_rescues(async_session)

    # Expected result
    expected_result = [family1, family2, family3]

    # Check result
    assert mammals_families == expected_result


# test for create_sunburst_data
def test_create_sunburst_data() -> None:

    # Create families
    flora_families = ["familyFlora", "familyFlora", "familyFlora2"]
    herpetofauna_families = [
            "familyHerpetofauna",
            "familyHerpetofauna",
            "familyHerpetofauna2"
            ]
    mammals_families = ["familyMammals", "familyMammals", "familyMammals2"]

    # create sunburst data
    sunburst_data = create_sunburst_data(
            flora_families,
            herpetofauna_families,
            mammals_families)

    # Expected result
    # Modificación del nodo 'Flora'
    flora_children = [
            SunburstBase(
                name="familyFlora",
                color="hsl(230,45%,45%)",
                loc=2, children=None
                ),
            SunburstBase(
                name="familyFlora2",
                color="hsl(230,50%,50%)",
                loc=1,
                children=None
                ),
            ]
    # Modificación del nodo 'Herpetofauna'
    herpetofauna_children = [
            SunburstBase(
                name="familyHerpetofauna",
                color="hsl(130,45%,45%)",
                loc=2,
                children=None
                ),
            SunburstBase(
                name="familyHerpetofauna2",
                color="hsl(130,50%,50%)",
                loc=1,
                children=None
                ),
            ]

    # Modificación del nodo 'Mamíferos'
    mammals_children = [
            SunburstBase(
                name="familyMammals",
                color="hsl(40,45%,45%)",
                loc=2,
                children=None
                ),
            SunburstBase(
                name="familyMammals2",
                color="hsl(40,50%,50%)",
                loc=1,
                children=None
                ),
            ]

    # Creando los nodos principales con el orden actualizado
    flora_node = SunburstBase(
            name="Flora",
            color="hsl(230,40%,40%)",
            loc=None,
            children=flora_children
            )
    herpetofauna_node = SunburstBase(
            name="Herpetofauna",
            color="hsl(130,40%,40%)",
            loc=None,
            children=herpetofauna_children
            )
    mammals_node = SunburstBase(
            name="Mamíferos",
            color="hsl(40,40%,40%)",
            loc=None,
            children=mammals_children
            )

    # Creando el nodo raíz con los nodos actualizados
    expected_result = SunburstBase(
        name="Rescates",
        color="hsl(0,0%,0%)",
        loc=None,
        children=[flora_node, herpetofauna_node, mammals_node]
    )

    print(f"sunburst_data: {sunburst_data}")
    print(f"expected_result: {expected_result}")

    # Check result
    assert sunburst_data == expected_result


# test for get_flora_families relocation
@pytest.mark.asyncio
async def test_get_flora_families_relocation(
        async_client: AsyncClient,
        async_session: AsyncSession
        ) -> None:

    # Create families
    specie1, genus1, family1, specieId1, genusId1, familyId1 = await create_specieWithFamily(async_client)
    specie2, genus2, family2, specieId2, genusId2, familyId2 = await create_specieWithFamily(async_client)
    specie3, genus3, family3, specieId3, genusId3, familyId3 = await create_specieWithFamily(async_client)

    RESCUE_ZONE_ID = await create_random_rescue_zone_id(async_client)
    RELOCATION_ZONE_ID = await create_random_relocation_zone_id(async_client)
    specie_id = await create_specie(async_client)

    # create flora rescue

    response = await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": "1",
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": "1.0",
            "rescue_area_longitude": "1.0",
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "is_epiphyte_confirmed": True,
            "is_bryophyte_confirmed": True,
            "specie_bryophyte_id": specieId1,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": None,
            "specie_epiphyte_id": specieId1,
            "genus_epiphyte_id": None,
            "family_epiphyte_id": None,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )

    assert response.status_code == 201
    id_rescue_flora1 = response.json()["id"]

    response = await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": "2",
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": "1.0",
            "rescue_area_longitude": "1.0",
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "is_epiphyte_confirmed": True,
            "is_bryophyte_confirmed": True,
            "specie_bryophyte_id": None,
            "genus_bryophyte_id": genusId2,
            "family_bryophyte_id": None,
            "specie_epiphyte_id": None,
            "genus_epiphyte_id": genusId2,
            "family_epiphyte_id": None,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )
    assert response.status_code == 201
    id_rescue_flora2 = response.json()["id"]

    response = await async_client.post(
        "/api/rescue_flora", json={
            "epiphyte_number": "3",
            "rescue_date": "2021-10-10T00:00:00",
            "rescue_area_latitude": "1.0",
            "rescue_area_longitude": "1.0",
            "substrate": "test_substrate",
            "dap_bryophyte": 1.0,
            "height_bryophyte": 1.0,
            "bryophyte_position": 1,
            "growth_habit": "test_growth_habit",
            "epiphyte_phenology": "test_epiphyte_phenology",
            "health_status_epiphyte": "test_health_status_epiphyte",
            "microhabitat": "test_microhabitat",
            "other_observations": "test_other_observations",
            "is_epiphyte_confirmed": True,
            "is_bryophyte_confirmed": True,
            "specie_bryophyte_id": None,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": familyId3,
            "specie_epiphyte_id": None,
            "genus_epiphyte_id": None,
            "family_epiphyte_id": familyId3,
            "rescue_zone_id": RESCUE_ZONE_ID,
        },
    )
    assert response.status_code == 201
    id_rescue_flora3 = response.json()["id"]

    # create flora relocations 1
    response = await async_client.post(
        "/api/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "relocation_number": "14",
            "size": 1.0,
            "epiphyte_phenology": "test_epiphyte_phenology14",
            "johanson_zone": "test_johanson_zone14",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "relocation_position_altitude": 14.0,
            "bryophyte_number": 14,
            "dap_bryophyte": 14.0,
            "height_bryophyte": 14.0,
            "bark_type": "test_bark_type14",
            "infested_lianas": "Poco",
            "other_observations": "test_other_observations14",
            "is_bryophyte_confirmed": True,
            "flora_rescue_id": id_rescue_flora1,
            "specie_bryophyte_id": specie_id,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": None,
            "relocation_zone_id": RELOCATION_ZONE_ID,
        },
    )
    assert response.status_code == 201, response.text

    # create flora relocations 2
    response = await async_client.post(
        "/api/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "relocation_number": "15",
            "size": 1.0,
            "epiphyte_phenology": "test_epiphyte_phenology14",
            "johanson_zone": "test_johanson_zone14",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "relocation_position_altitude": 14.0,
            "bryophyte_number": 14,
            "dap_bryophyte": 14.0,
            "height_bryophyte": 14.0,
            "bark_type": "test_bark_type14",
            "infested_lianas": "Poco",
            "other_observations": "test_other_observations14",
            "is_bryophyte_confirmed": True,
            "flora_rescue_id": id_rescue_flora2,
            "specie_bryophyte_id": specie_id,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": None,
            "relocation_zone_id": RELOCATION_ZONE_ID,
        },
    )
    assert response.status_code == 201, response.text

    # create flora relocations 3
    response = await async_client.post(
        "/api/flora_relocation", json={
            "relocation_date": "2021-12-10T00:00:00",
            "relocation_number": "16",
            "size": 1.0,
            "epiphyte_phenology": "test_epiphyte_phenology14",
            "johanson_zone": "test_johanson_zone14",
            "relocation_position_latitude": create_latitude(),
            "relocation_position_longitude": create_longitude(),
            "relocation_position_altitude": 14.0,
            "bryophyte_number": 14,
            "dap_bryophyte": 14.0,
            "height_bryophyte": 14.0,
            "bark_type": "test_bark_type14",
            "infested_lianas": "Poco",
            "other_observations": "test_other_observations14",
            "is_bryophyte_confirmed": True,
            "flora_rescue_id": id_rescue_flora3,
            "specie_bryophyte_id": specie_id,
            "genus_bryophyte_id": None,
            "family_bryophyte_id": None,
            "relocation_zone_id": RELOCATION_ZONE_ID,
        },
    )
    assert response.status_code == 201, response.text

    # Get flora families relocation
    flora_families = await get_flora_families_relocation(async_session)

    # Expected result
    expected_result = [family1, family2, family3]

    assert flora_families == expected_result


# test for get_herpetofauna_families_relocation
@pytest.mark.asyncio
async def test_get_herpetofauna_families_relocation(
        async_client: AsyncClient,
        async_session: AsyncSession
        ) -> None:

    # Create families
    specie1, genus1, family1, specieId1, genusId1, familyId1 = await create_specieWithFamily(async_client)
    specie2, genus2, family2, specieId2, genusId2, familyId2 = await create_specieWithFamily(async_client)
    specie3, genus3, family3, specieId3, genusId3, familyId3 = await create_specieWithFamily(async_client)

    # Create transect herpetofauna translocation
    transect_herpetofauna_translocation_id: int = await create_transect_herpetofauna_translocation(async_client)

    # Create point herpetofauna translocation
    point_herpetofauna_translocation_id: int = await create_point_herpetofauna_translocation(async_client)

    # Create mark herpetofauna
    mark_herpetofauna_id: int = await create_mark_herpetofauna(async_client)

    # Create translocations herpetofauna
    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": "1",
            "transect_herpetofauna_translocation_id": transect_herpetofauna_translocation_id,
            "point_herpetofauna_translocation_id": point_herpetofauna_translocation_id,
            "specie_id": specieId1,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    assert response.status_code == 201

    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": "2",
            "transect_herpetofauna_translocation_id": transect_herpetofauna_translocation_id,
            "point_herpetofauna_translocation_id": point_herpetofauna_translocation_id,
            "specie_id": specieId2,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    assert response.status_code == 201

    response: Response = await async_client.post(
        "/api/translocation_herpetofauna", json={
            "cod": "3",
            "transect_herpetofauna_translocation_id": transect_herpetofauna_translocation_id,
            "point_herpetofauna_translocation_id": point_herpetofauna_translocation_id,
            "specie_id": specieId3,
            "mark_herpetofauna_id": mark_herpetofauna_id,
        },
    )
    assert response.status_code == 201

    # Get herpetofauna families relocation
    herpetofauna_families = await get_herpetofauna_families_relocation(
            async_session
            )

    # Expected result
    expected_result = [family1, family2, family3]

    # Check result
    assert herpetofauna_families == expected_result


# test for get_mammals_families_relocation
@pytest.mark.asyncio
async def test_get_mammals_families_relocation(
        async_client: AsyncClient,
        async_session: AsyncSession
        ) -> None:

    # Create families
    specie1, genus1, family1, specieId1, genusId1, familyId1 = await create_specieWithFamily(async_client)
    specie2, genus2, family2, specieId2, genusId2, familyId2 = await create_specieWithFamily(async_client)
    specie3, genus3, family3, specieId3, genusId3, familyId3 = await create_specieWithFamily(async_client)

    habitat_id = await create_habitat(async_client)
    age_group_id = await create_age_group(async_client)

    # Create rescues
    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": "1",
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": specieId1,
            "genus_id": None
        },
    )
    assert response.status_code == 201
    rescue_id1 = response.json()["id"]

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": "2",
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": specieId2,
            "genus_id": None
        },
    )
    assert response.status_code == 201
    rescue_id2 = response.json()["id"]

    response = await async_client.post(
        "api/rescue_mammals", json={
            "cod": "3",
            "date": "2021-10-10T00:00:00",
            "mark": "mark",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "gender": True,
            "LT": 1.0,
            "LC": 1.0,
            "LP": 1.0,
            "LO": 1.0,
            "LA": 1.0,
            "weight": 10,
            "observation": "observation",
            "is_specie_confirmed": True,
            "habitat_id": habitat_id,
            "age_group_id": age_group_id,
            "specie_id": None,
            "genus_id": genusId3
        },
    )
    assert response.status_code == 201
    rescue_id3 = response.json()["id"]

    site_release_mammals_id: int = await create_site_release(async_client)

    # Create mammals relocations
    response = await async_client.post(
        "api/release_mammals", json={
            "cod": "1",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_id1,
        }
    )
    assert response.status_code == 201

    response = await async_client.post(
        "api/release_mammals", json={
            "cod": "2",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_id2,
        }
    )

    assert response.status_code == 201

    response = await async_client.post(
        "api/release_mammals", json={
            "cod": "3",
            "longitude": 1.0,
            "latitude": 1.0,
            "altitude": 10,
            "sustrate": "substrate",
            "site_release_mammals_id": site_release_mammals_id,
            "rescue_mammals_id": rescue_id3,
        }
    )

    assert response.status_code == 201

    # Get mammals families relocation
    mammals_families = await get_mammals_families_relocation(async_session)

    # Expected result
    expected_result = [family1, family2, family3]

    # Check result
    assert mammals_families == expected_result
