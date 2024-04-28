from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.species import (
        get_specie_by_id,
        get_genus_by_id,
        get_family_by_id,
        )
from app.crud.rescue_flora import (
        get_all_flora_rescues
        )
from app.crud.rescue_herpetofauna import (
        get_all_rescue_herpetofauna
        )

from app.crud.rescue_mammals import (
        get_rescue_mammals
        )

from app.schemas.nivo import (
        SunburstBase,
        ColorHSLBase,
        )


# Create SunburstBase children
def create_sunburst_base_children(
        name: str,
        children: List[str],
        color: str,
        ) -> SunburstBase:
    loc: int = 0
    for child in children:
        if child == name:
            loc += 1
        else:
            pass
    result = SunburstBase(
            name=name,
            color=color,
            loc=loc,
            children=None
            )
    return result


# Get list of families in flora rescues
async def get_flora_families(
        db: AsyncSession,
        ) -> List[str]:
    flora_families: List[str] = []
    flora_rescues_db = await get_all_flora_rescues(db)
    for rescue in flora_rescues_db:
        if rescue.family_epiphyte_id:
            family = await get_family_by_id(db, rescue.family_epiphyte_id)
            if family:
                flora_families.append(family.family_name)
            else:
                pass
        if rescue.genus_epiphyte_id:
            genus = await get_genus_by_id(db, rescue.genus_epiphyte_id)
            if genus:
                family = await get_family_by_id(db, genus.family_id)
                if family:
                    flora_families.append(family.family_name)
                else:
                    pass
            else:
                pass
        else:
            species = await get_specie_by_id(db, rescue.specie_epiphyte_id)
            if species:
                genus = await get_genus_by_id(db, species.genus_id)
                if genus:
                    family = await get_family_by_id(db, genus.family_id)
                    if family:
                        flora_families.append(family.family_name)
                    else:
                        pass
                else:
                    pass

    return flora_families


# Get list of families in herpetofauna rescues
async def get_herpetofauna_families(
        db: AsyncSession,
        ) -> List[str]:
    herpetofauna_families: List[str] = []
    herpetofauna_rescues_db = await get_all_rescue_herpetofauna(db)
    for rescue in herpetofauna_rescues_db:
        specie = await get_specie_by_id(db, rescue.specie_id)
        if specie:
            genus = await get_genus_by_id(db, specie.genus_id)
            if genus:
                family = await get_family_by_id(db, genus.family_id)
                if family:
                    herpetofauna_families.append(family.family_name)
                else:
                    pass
            else:
                pass
        else:
            pass

    return herpetofauna_families


# Get list of families in mammals rescues
async def get_mammals_families(
        db: AsyncSession,
        ) -> List[str]:
    mammals_families: List[str] = []
    mammals_rescues_db = await get_rescue_mammals(db)
    for rescue in mammals_rescues_db:
        if rescue.specie_id:
            specie = await get_specie_by_id(db, rescue.specie_id)
            if specie:
                genus = await get_genus_by_id(db, specie.genus_id)
                if genus:
                    family = await get_family_by_id(db, genus.family_id)
                    if family:
                        mammals_families.append(family.family_name)
                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            genus = await get_genus_by_id(db, rescue.genus_id)
            if genus:
                family = await get_family_by_id(db, genus.family_id)
                if family:
                    mammals_families.append(family.family_name)
                else:
                    pass
            else:
                pass

    return mammals_families


# Create sunburst data
def create_sunburst_data(
        flora_families: List[str],
        herpetofauna_families: List[str],
        mammals_families: List[str],
        ) -> SunburstBase:

    # create flora rescue set
    flora_families_set: set = set(flora_families)
    flora_families_sorted = sorted(flora_families_set)

    # create herpetofauna rescue set
    herpetofauna_families_set: set = set(herpetofauna_families)
    herpetofauna_families_sorted = sorted(herpetofauna_families_set)

    # create mammals rescue list set
    mammals_families_set: set = set(mammals_families)
    mammals_families_sorted = sorted(mammals_families_set)

    COLOR_FLORA: dict = {
            "h": 230,
            "s": 40,
            "l": 40
            }

    COLOR_HERPETOFAUNA: dict = {
            "h": 130,
            "s": 40,
            "l": 40
            }

    COLOR_MAMMALS: dict = {
            "h": 40,
            "s": 40,
            "l": 40
            }

    # make children of rescue flora
    flora_children: List[SunburstBase] = []
    addColor = 5
    for family in flora_families_sorted:
        # create color
        color_hsl: ColorHSLBase = ColorHSLBase(
                h=COLOR_FLORA["h"],
                s=COLOR_FLORA["s"]+addColor,
                l=COLOR_FLORA["l"]+addColor
                )
        if addColor < 80:
            addColor += 5
        else:
            pass
        # create children
        children = create_sunburst_base_children(
                family,
                flora_families,
                color=f"hsl({color_hsl.h},{color_hsl.s}%,{color_hsl.l}%)"
                )
        flora_children.append(children)

    # make children of rescue herpetofauna
    herpetofauna_children: List[SunburstBase] = []
    addColor = 5
    for family in herpetofauna_families_sorted:
        # create color
        color_hsl: ColorHSLBase = ColorHSLBase(
                h=COLOR_HERPETOFAUNA["h"],
                s=COLOR_HERPETOFAUNA["s"]+addColor,
                l=COLOR_HERPETOFAUNA["l"]+addColor
                )
        if addColor < 80:
            addColor += 5
        else:
            pass
        # create children
        children = create_sunburst_base_children(
                family,
                herpetofauna_families,
                color=f"hsl({color_hsl.h},{color_hsl.s}%,{color_hsl.l}%)"
                )
        herpetofauna_children.append(children)

    # make children of rescue mammals
    mammals_children: List[SunburstBase] = []
    addColor = 5
    for family in mammals_families_sorted:
        # create color
        color_hsl: ColorHSLBase = ColorHSLBase(
                h=COLOR_MAMMALS["h"],
                s=COLOR_MAMMALS["s"]+addColor,
                l=COLOR_MAMMALS["l"]+addColor
                )
        if addColor < 80:
            addColor += 5
        else:
            pass
        # create children
        children = create_sunburst_base_children(
                family,
                mammals_families,
                color=f"hsl({color_hsl.h},{color_hsl.s}%,{color_hsl.l}%)"
                )
        mammals_children.append(children)

    # make SuburstBase global
    sunburst_data: SunburstBase = SunburstBase(
            name="Rescates",
            color="hsl(0,0%,0%)",
            loc=None,
            children=[
                SunburstBase(
                    name="Flora",
                    color="hsl(230,40%,40%)",
                    loc=None,
                    children=flora_children
                    ),
                SunburstBase(
                    name="Herpetofauna",
                    color="hsl(130,40%,40%)",
                    loc=None,
                    children=herpetofauna_children
                    ),
                SunburstBase(
                    name="Mamíferos",
                    color="hsl(40,40%,40%)",
                    loc=None,
                    children=mammals_children
                    )
                ]
            )

    return sunburst_data
