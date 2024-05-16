from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException

from app.schemas.rescue_mammals import (
    # Habitat
    HabitatCreate,

    # RescueMammal
    RescueMammalsCreate,

    # SiteRelease
    SiteReleaseMammalsCreate,

    # ReleaseMammals
    ReleaseMammalsCreate,

    # RescueMammalsWithSpecie
    RescueMammalsWithSpecie,
    RescueMammalsWithSpecieExtended,

    # RealeaseMammalsWithSpecie
    ReleaseMammalsWithSpecie,
)

from app.models.rescue_mammals import (
    Habitat,
    RescueMammals,
    SiteReleaseMammals,
    ReleaseMammals,
)

from app.crud.species import (
        get_specie_by_id,
        get_genus_by_id
)

from app.crud.rescue_herpetofauna import get_age_group_by_id

# Purpose: CRUD operations for RescueMammals

"""
CRUD HABITAT
"""


# Get if habitat name exists
async def get_habitat_name(db: AsyncSession, name: str) -> Habitat | None:
    result = await db.execute(select(Habitat).filter(Habitat.name == name))
    return result.scalars().first()


# Get habitat by id
async def get_habitat_id(db: AsyncSession, id: int) -> Habitat | None:
    result = await db.execute(select(Habitat).filter(Habitat.id == id))
    return result.scalars().first()


# Get all habitats
async def get_habitats(db: AsyncSession) -> List[Habitat]:
    result = await db.execute(select(Habitat))
    return list(result.scalars().all())


# Create habitat
async def create_habitat(db: AsyncSession, habitat: HabitatCreate) -> Habitat:
    habitat_db = Habitat(
        name=habitat.name,
    )
    db.add(habitat_db)
    await db.commit()
    await db.refresh(habitat_db)
    return habitat_db


# Update habitat
async def update_habitat(
        db: AsyncSession,
        habitat_id: int,
        habitat_update: HabitatCreate
        ) -> Habitat:
    result = await db.execute(select(Habitat).where(Habitat.id == habitat_id))
    habitat_db = result.scalars().first()
    if habitat_db is None:
        raise HTTPException(status_code=404, detail="Habitat not found")
    habitat_db.name = habitat_update.name
    await db.commit()
    await db.refresh(habitat_db)
    return habitat_db


# Delete habitat
async def delete_habitat(db: AsyncSession, habitat_id: int) -> Habitat:
    result = await db.execute(select(Habitat).where(Habitat.id == habitat_id))
    habitat_db = result.scalars().first()
    if habitat_db is None:
        raise HTTPException(status_code=404, detail="Habitat not found")
    await db.execute(delete(Habitat).where(Habitat.id == habitat_id))
    await db.commit()
    return habitat_db

"""
CRUD RESCUE MAMMALS
"""


# Get if rescue mammal cod exists
async def get_rescue_mammal_cod(
        db: AsyncSession,
        cod: str
        ) -> RescueMammals | None:
    result = await db.execute(
            select(RescueMammals).filter(RescueMammals.cod == cod)
            )
    return result.scalars().first()


# Get rescue mammal by id
async def get_rescue_mammal_id(
        db: AsyncSession,
        id: int
        ) -> RescueMammals | None:
    result = await db.execute(
            select(RescueMammals).filter(RescueMammals.id == id)
            )
    return result.scalars().first()


# Get all rescue mammals
async def get_rescue_mammals(db: AsyncSession) -> List[RescueMammals]:
    result = await db.execute(select(RescueMammals))
    return list(result.scalars().all())


# Create rescue mammal
async def create_rescue_mammal(
        db: AsyncSession,
        rescue_mammal: RescueMammalsCreate
        ) -> RescueMammals:
    rescue_mammal_db = RescueMammals(
        cod=rescue_mammal.cod,
        date=rescue_mammal.date,
        mark=rescue_mammal.mark,
        longitude=rescue_mammal.longitude,
        latitude=rescue_mammal.latitude,
        altitude=rescue_mammal.altitude,
        gender=rescue_mammal.gender,
        LT=rescue_mammal.LT,
        LC=rescue_mammal.LC,
        LP=rescue_mammal.LP,
        LO=rescue_mammal.LO,
        LA=rescue_mammal.LA,
        weight=rescue_mammal.weight,
        observation=rescue_mammal.observation,
        is_specie_confirmed=rescue_mammal.is_specie_confirmed,
        habitat_id=rescue_mammal.habitat_id,
        age_group_id=rescue_mammal.age_group_id,
        specie_id=rescue_mammal.specie_id,
        genus_id=rescue_mammal.genus_id,
    )
    db.add(rescue_mammal_db)
    await db.commit()
    await db.refresh(rescue_mammal_db)
    return rescue_mammal_db


# Update rescue mammal
async def update_rescue_mammal(
        db: AsyncSession,
        rescue_mammal_id: int,
        rescue_mammal_update: RescueMammalsCreate
        ) -> RescueMammals:
    result = await db.execute(
            select(RescueMammals).where(RescueMammals.id == rescue_mammal_id)
            )
    rescue_mammal_db = result.scalars().first()
    if rescue_mammal_db is None:
        raise HTTPException(status_code=404, detail="Rescue Mammal not found")
    rescue_mammal_db.cod = rescue_mammal_update.cod
    rescue_mammal_db.date = rescue_mammal_update.date
    rescue_mammal_db.mark = rescue_mammal_update.mark
    rescue_mammal_db.longitude = rescue_mammal_update.longitude
    rescue_mammal_db.latitude = rescue_mammal_update.latitude
    rescue_mammal_db.altitude = rescue_mammal_update.altitude
    rescue_mammal_db.gender = rescue_mammal_update.gender
    rescue_mammal_db.LT = rescue_mammal_update.LT
    rescue_mammal_db.LC = rescue_mammal_update.LC
    rescue_mammal_db.LP = rescue_mammal_update.LP
    rescue_mammal_db.LO = rescue_mammal_update.LO
    rescue_mammal_db.LA = rescue_mammal_update.LA
    rescue_mammal_db.weight = rescue_mammal_update.weight
    rescue_mammal_db.observation = rescue_mammal_update.observation
    rescue_mammal_db.is_specie_confirmed = rescue_mammal_update.is_specie_confirmed
    rescue_mammal_db.habitat_id = rescue_mammal_update.habitat_id
    rescue_mammal_db.age_group_id = rescue_mammal_update.age_group_id
    rescue_mammal_db.specie_id = rescue_mammal_update.specie_id
    rescue_mammal_db.genus_id = rescue_mammal_update.genus_id
    await db.commit()
    await db.refresh(rescue_mammal_db)
    return rescue_mammal_db


# Delete rescue mammal
async def delete_rescue_mammal(
        db: AsyncSession,
        rescue_mammal_id: int) -> RescueMammals:
    result = await db.execute(
            select(RescueMammals).where(RescueMammals.id == rescue_mammal_id)
            )
    rescue_mammal_db = result.scalars().first()
    if rescue_mammal_db is None:
        raise HTTPException(status_code=404, detail="Rescue Mammal not found")
    await db.execute(
            delete(RescueMammals).where(RescueMammals.id == rescue_mammal_id)
            )
    await db.commit()
    return rescue_mammal_db

"""
CRUD SITE RELEASE MAMMALS
"""


# Get if site release mammal name exists
async def get_site_release_mammal_name(
        db: AsyncSession,
        name: str
        ) -> SiteReleaseMammals | None:
    result = await db.execute(
            select(SiteReleaseMammals).filter(SiteReleaseMammals.name == name)
            )
    return result.scalars().first()


# Get site release mammal by id
async def get_site_release_mammal_id(
        db: AsyncSession,
        id: int
        ) -> SiteReleaseMammals | None:
    result = await db.execute(
            select(SiteReleaseMammals).filter(SiteReleaseMammals.id == id)
            )
    return result.scalars().first()


# Get all site release mammals
async def get_site_release_mammals(
        db: AsyncSession
        ) -> List[SiteReleaseMammals]:
    result = await db.execute(select(SiteReleaseMammals))
    return list(result.scalars().all())


# Create site release mammal
async def create_site_release_mammal(
        db: AsyncSession,
        site_release_mammal: SiteReleaseMammalsCreate
        ) -> SiteReleaseMammals:
    site_release_mammal_db = SiteReleaseMammals(
        name=site_release_mammal.name,
    )
    db.add(site_release_mammal_db)
    await db.commit()
    await db.refresh(site_release_mammal_db)
    return site_release_mammal_db


# Update site release mammal
async def update_site_release_mammal(
        db: AsyncSession,
        site_release_mammal_id: int,
        site_release_mammal_update: SiteReleaseMammalsCreate
        ) -> SiteReleaseMammals:
    result = await db.execute(
            select(SiteReleaseMammals).where(
                SiteReleaseMammals.id == site_release_mammal_id
                ))
    site_release_mammal_db = result.scalars().first()
    if site_release_mammal_db is None:
        raise HTTPException(
                status_code=404,
                detail="Site Release Mammal not found"
                )
    site_release_mammal_db.name = site_release_mammal_update.name
    await db.commit()
    await db.refresh(site_release_mammal_db)
    return site_release_mammal_db


# Delete site release mammal
async def delete_site_release_mammal(
        db: AsyncSession,
        site_release_mammal_id: int
        ) -> SiteReleaseMammals:
    result = await db.execute(
            select(SiteReleaseMammals).where(
                SiteReleaseMammals.id == site_release_mammal_id
                ))
    site_release_mammal_db = result.scalars().first()
    if site_release_mammal_db is None:
        raise HTTPException(
                status_code=404,
                detail="Site Release Mammal not found"
                )
    await db.execute(
            delete(SiteReleaseMammals).where(
                SiteReleaseMammals.id == site_release_mammal_id
                ))
    await db.commit()
    return site_release_mammal_db

"""
CRUD RELEASE MAMMALS
"""


# Get if release mammal cod exists
async def get_release_mammal_cod(
        db: AsyncSession,
        cod: str
        ) -> ReleaseMammals | None:
    result = await db.execute(
            select(ReleaseMammals).filter(ReleaseMammals.cod == cod)
            )
    return result.scalars().first()


# Get release mammal by id
async def get_release_mammal_id(
        db: AsyncSession,
        id: int
        ) -> ReleaseMammals | None:
    result = await db.execute(
            select(
                ReleaseMammals).filter(ReleaseMammals.id == id
                                       ))
    return result.scalars().first()


# Get all release mammals
async def get_release_mammals(db: AsyncSession) -> List[ReleaseMammals]:
    result = await db.execute(select(ReleaseMammals))
    return list(result.scalars().all())


# Create release mammal
async def create_release_mammal(
        db: AsyncSession,
        release_mammal: ReleaseMammalsCreate
        ) -> ReleaseMammals:
    release_mammal_db = ReleaseMammals(
        cod=release_mammal.cod,
        longitude=release_mammal.longitude,
        latitude=release_mammal.latitude,
        altitude=release_mammal.altitude,
        sustrate=release_mammal.sustrate,
        site_release_mammals_id=release_mammal.site_release_mammals_id,
        rescue_mammals_id=release_mammal.rescue_mammals_id,
    )
    db.add(release_mammal_db)
    await db.commit()
    await db.refresh(release_mammal_db)
    return release_mammal_db


# Update release mammal
async def update_release_mammal(
        db: AsyncSession,
        release_mammal_id: int,
        release_mammal_update: ReleaseMammalsCreate
        ) -> ReleaseMammals:
    result = await db.execute(
            select(ReleaseMammals).where(
                ReleaseMammals.id == release_mammal_id
                ))
    release_mammal_db = result.scalars().first()
    if release_mammal_db is None:
        raise HTTPException(status_code=404, detail="Release Mammal not found")
    release_mammal_db.cod = release_mammal_update.cod
    release_mammal_db.longitude = release_mammal_update.longitude
    release_mammal_db.latitude = release_mammal_update.latitude
    release_mammal_db.altitude = release_mammal_update.altitude
    release_mammal_db.sustrate = release_mammal_update.sustrate
    release_mammal_db.site_release_mammals_id = release_mammal_update.site_release_mammals_id
    release_mammal_db.rescue_mammals_id = release_mammal_update.rescue_mammals_id
    await db.commit()
    await db.refresh(release_mammal_db)
    return release_mammal_db


# Delete release mammal
async def delete_release_mammal(
        db: AsyncSession, release_mammal_id: int) -> ReleaseMammals:
    result = await db.execute(
            select(ReleaseMammals).where(
                ReleaseMammals.id == release_mammal_id
                ))
    release_mammal_db = result.scalars().first()
    if release_mammal_db is None:
        raise HTTPException(status_code=404, detail="Release Mammal not found")
    await db.execute(
            delete(ReleaseMammals).where(
                ReleaseMammals.id == release_mammal_id
                ))
    await db.commit()
    return release_mammal_db

"""
CRUD RESCUE MAMMALS WITH SPECIE
"""


# Get rescue mammals with specie
async def get_rescue_mammals_with_specie(
        db: AsyncSession
        ) -> List[RescueMammalsWithSpecie]:
    rescues = await get_rescue_mammals(db)

    result = []

    for rescue in rescues:
        specie_db = await get_specie_by_id(db, rescue.specie_id)
        specie_name: str | None
        if specie_db:
            specie_name = specie_db.specific_epithet
        else:
            specie_name = None

        genus_db = await get_genus_by_id(db, rescue.genus_id)
        genus_name: str | None
        if genus_db:
            genus_name = genus_db.genus_name
        else:
            genus_name = None
        result.append(RescueMammalsWithSpecie(
            cod=rescue.cod,
            date=rescue.date,
            longitude=rescue.longitude,
            latitude=rescue.latitude,
            observation=rescue.observation,
            specie_name=specie_name,
            genus_name=genus_name,
        ))
    return result


# Get rescue mammal with specie by id
async def get_rescue_mammal_with_specie_id(
        db: AsyncSession,
        id: int
        ) -> RescueMammalsWithSpecie:
    """
    Get rescue mammal with specie by id
    db -> database connection
    id -> id of rescue mammal

    return -> RescueMammalsWithSpecie

    """
    rescue = await get_rescue_mammal_id(db, id)
    if rescue is None:
        raise HTTPException(status_code=404, detail="Rescue Mammal not found")

    specie_db = await get_specie_by_id(db, rescue.specie_id)
    specie_name: str | None
    if specie_db:
        specie_name = specie_db.specific_epithet
    else:
        specie_name = None

    genus_db = await get_genus_by_id(db, rescue.genus_id)
    genus_name: str | None
    if genus_db:
        genus_name = genus_db.genus_name
    else:
        genus_name = None

    return RescueMammalsWithSpecie(
        cod=rescue.cod,
        date=rescue.date,
        longitude=rescue.longitude,
        latitude=rescue.latitude,
        observation=rescue.observation,
        specie_name=specie_name,
        genus_name=genus_name,
    )


# Get rescue mammal list with specie by specie id
async def get_rescue_mammal_list_with_specie_by_specie_id(
        db: AsyncSession,
        specie_id: int
        ) -> List[RescueMammalsWithSpecie]:
    """
    Get rescue mammal list with specie by specie id
    db -> database connection
    specie_id -> id of specie

    return -> List[RescueMammalsWithSpecie]

    """
    rescues = await db.execute(
            select(RescueMammals).filter(RescueMammals.specie_id == specie_id)
            )
    rescues_db = rescues.scalars().all()

    result = []

    for rescue in rescues_db:
        specie_name: str | None
        genus_name: str | None
        specie_db = await get_specie_by_id(db, rescue.specie_id)
        if specie_db:
            specie_name = specie_db.specific_epithet
            genus_name = None
        else:
            specie_name = None
            genus_db = await get_genus_by_id(db, rescue.genus_id)
            if genus_db:
                genus_name = genus_db.genus_name
            else:
                genus_name = None

        result.append(RescueMammalsWithSpecie(
            cod=rescue.cod,
            date=rescue.date,
            longitude=rescue.longitude,
            latitude=rescue.latitude,
            observation=rescue.observation,
            specie_name=specie_name,
            genus_name=genus_name,
        ))
    return result


# Get all realease mammals with specie
async def get_release_mammals_with_specie(
        db: AsyncSession
        ) -> List[ReleaseMammalsWithSpecie]:
    releases = await get_release_mammals(db)

    result = []

    for release in releases:
        rescue_db = await get_rescue_mammal_id(db, release.rescue_mammals_id)
        if rescue_db is None:
            raise HTTPException(
                    status_code=404,
                    detail="Rescue Mammal not found"
                    )

        specie_db = await get_specie_by_id(db, rescue_db.specie_id)
        specie_name: str | None
        if specie_db:
            specie_name = specie_db.specific_epithet
        else:
            specie_name = None

        genus_db = await get_genus_by_id(db, rescue_db.genus_id)
        genus_name: str | None
        if genus_db:
            genus_name = genus_db.genus_name
        else:
            genus_name = None

        site_release_db = await get_site_release_mammal_id(
                db, release.site_release_mammals_id
                )
        if site_release_db:
            site_release_mammals = site_release_db.name
        else:
            raise HTTPException(
                    status_code=404,
                    detail="Site Release Mammal not found"
                    )

        result.append(ReleaseMammalsWithSpecie(
            cod=release.cod,
            longitude=release.longitude,
            latitude=release.latitude,
            altitude=release.altitude,
            sustrate=release.sustrate,
            site_release_mammals=site_release_mammals,
            specie_name=specie_name,
            genus_name=genus_name,
        ))
    return result


# Get rescue mammal with specie by code rescue
async def get_rescue_mammal_with_specie_by_cod(
        db: AsyncSession,
        rescue_cod: str
        ) -> RescueMammalsWithSpecieExtended:
    """
    Get rescue mammal with specie by code rescue
    """
    rescue = await get_rescue_mammal_cod(db, rescue_cod)
    if rescue is None:
        raise HTTPException(
                status_code=404,
                detail="Rescue Mammal not found"
                )

    specie_name: str | None
    genus_name: str | None = None
    specie_db = await get_specie_by_id(db, rescue.specie_id)
    if specie_db:
        specie_name = specie_db.specific_epithet
        genus_db = await get_genus_by_id(db, specie_db.genus_id)
        if genus_db:
            genus_name = genus_db.genus_name
    else:
        specie_name = None
        genus_db = await get_genus_by_id(db, rescue.genus_id)
        if genus_db:
            genus_name = genus_db.genus_name

    gender: str | None = None
    if rescue.gender is True:
        gender = "Macho"
    elif rescue.gender is False:
        gender = "Hembra"

    habitat_db = await get_habitat_id(db, rescue.habitat_id)
    if habitat_db:
        habitat_name = habitat_db.name
    else:
        habitat_name = None

    age_group_db = await get_age_group_by_id(db, rescue.age_group_id)
    if age_group_db:
        age_group_name = age_group_db.name
    else:
        age_group_name = None

    return RescueMammalsWithSpecieExtended(
        cod=rescue.cod,
        date=rescue.date,
        longitude=rescue.longitude,
        latitude=rescue.latitude,
        observation=rescue.observation,
        specie_name=specie_name,
        genus_name=genus_name,
        mark=rescue.mark,
        gender=gender,
        LT=rescue.LT,
        LC=rescue.LC,
        LP=rescue.LP,
        LO=rescue.LO,
        LA=rescue.LA,
        weight=rescue.weight,
        habitat_name=habitat_name,
        age_group_name=age_group_name,
    )


# Get all realease mammals with specie by cod
async def get_release_mammals_with_specie_by_cod(
        db: AsyncSession,
        rescue_cod: str
        ) -> ReleaseMammalsWithSpecie:
    rescue_db = await get_rescue_mammal_cod(db, rescue_cod)
    if rescue_db is None:
        raise HTTPException(
                status_code=404,
                detail="Rescue Mammal not found"
                )
    release_db = await db.execute(
            select(ReleaseMammals).filter(
                ReleaseMammals.rescue_mammals_id == rescue_db.id
                )
            )
    release = release_db.scalars().first()
    if release is None:
        raise HTTPException(
                status_code=404,
                detail="Release Mammal not found"
                )
    specie_db = await get_specie_by_id(db, rescue_db.specie_id)
    specie_name: str | None
    genus_name: str | None
    if specie_db:
        specie_name = specie_db.specific_epithet
        genus_db = await get_genus_by_id(db, specie_db.genus_id)
        if genus_db:
            genus_name = genus_db.genus_name
        else:
            genus_name = None
    else:
        specie_name = None
        genus_db = await get_genus_by_id(db, rescue_db.genus_id)
        if genus_db:
            genus_name = genus_db.genus_name
        else:
            genus_name = None

    site_release_db = await get_site_release_mammal_id(
            db, release.site_release_mammals_id
            )
    if site_release_db:
        site_release_mammals = site_release_db.name
    else:
        raise HTTPException(
                status_code=404,
                detail="Site Release Mammal not found"
                )
    return ReleaseMammalsWithSpecie(
            cod=release.cod,
            longitude=release.longitude,
            latitude=release.latitude,
            altitude=release.altitude,
            sustrate=release.sustrate,
            site_release_mammals=site_release_mammals,
            specie_name=specie_name,
            genus_name=genus_name,
            )
