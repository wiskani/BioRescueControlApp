from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.crud.species import (
        get_specie_by_id,
        get_genus_by_id,
        get_family_by_id,
        )
from app.crud.rescue_flora import (
        get_all_flora_rescues,
        get_all_flora_relocations,
        get_flora_rescue_by_id
        )
from app.crud.rescue_herpetofauna import (
        get_all_rescue_herpetofauna,
        get_all_translocation_herpetofauna
        )

from app.crud.rescue_mammals import (
        get_rescue_mammals,
        get_release_mammals
        )


# Get list of families in flora rescues
async def get_flora_families_rescues(
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
async def get_herpetofauna_families_rescues(
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
async def get_mammals_families_rescues(
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


# Get list of families in flora relocations
async def get_flora_families_relocation(
        db: AsyncSession,
        ) -> List[str]:
    flora_families: List[str] = []
    flora_relocation_db = await get_all_flora_relocations(db)
    for relocation in flora_relocation_db:
        if relocation.flora_rescue_id:
            rescue = await get_flora_rescue_by_id(
                    db,
                    relocation.flora_rescue_id
                    )
            if rescue:
                if rescue.family_epiphyte_id:
                    family = await get_family_by_id(
                            db,
                            rescue.family_epiphyte_id
                            )
                    if family:
                        flora_families.append(family.family_name)
                    else:
                        pass
                if rescue.genus_epiphyte_id:
                    genus = await get_genus_by_id(
                            db,
                            rescue.genus_epiphyte_id
                            )
                    if genus:
                        family = await get_family_by_id(
                                db,
                                genus.family_id
                                )
                        if family:
                            flora_families.append(family.family_name)
                        else:
                            pass
                    else:
                        pass
                else:
                    species = await get_specie_by_id(
                            db,
                            rescue.specie_epiphyte_id
                            )
                    if species:
                        genus = await get_genus_by_id(db, species.genus_id)
                        if genus:
                            family = await get_family_by_id(
                                    db,
                                    genus.family_id
                                    )
                            if family:
                                flora_families.append(family.family_name)
                            else:
                                pass
                        else:
                            pass
        else:
            pass
    return flora_families
