from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union
from fastapi.responses import JSONResponse
import pandas as pd


from app.api.deps import PermissonsChecker, get_db

#CRUD
from app.crud.rescue_flora import (
    create_plant_nursery,
    create_flora_relocation,
    create_flora_rescue,
    get_flora_rescue,
    get_plant_nursery,
    get_flora_relocation,
    )
from app.crud.tower import create_tower, get_tower_by_number
from app.crud.rescue_herpetofauna import(
    create_transect_herpetofauna,
    get_transect_herpetofauna_by_number,
    create_rescue_herpetofauna,
    get_rescue_herpetofauna_by_number,
    create_mark_herpetofauna,
    get_mark_herpetofauna_by_number,
    create_transect_herpetofauna_translocation,
    get_transect_herpetofauna_translocation_by_cod,
    create_point_herpetofauna_translocation,
    get_point_herpetofauna_translocation_by_cod,
    create_translocation_herpetofauna,
    get_translocation_herpetofauna_by_cod
)

#Schemas
from app.schemas.rescue_flora import (
    PlantNurseryBase,
    FloraRelocationBase,
    FloraRescueBase,
    )
from app.schemas.rescue_herpetofauna import (
    TransectHerpetofaunaCreate,
    RescueHerpetofaunaCreate,
    MarkHerpetofaunaCreate,
    TransectHerpetofaunaTranslocationCreate,
    PointHerpetofaunaTranslocationCreate,
    TranslocationHerpetofaunaCreate
)
from app.schemas.towers import TowerBase
from app.schemas.services import UTMData

from app.services.files import (
    convert_to_datetime,
    remplace_nan_with_none,
    none_value,
    insertGEOData,
    addIdSpecieByName,
    addIdGenusByName,
    addIdFamilyByName,
    addBooleanByGender,
    addMarkIdByNumber,
    addAgeGroupIdByName,
    addTransectIdByNumber,
    addNumRescueHerpeto,
    addBooleanByCheck,
    addRescueIdByNumber,
    addTransectTranslocationIdByCod,
    addPointTranslocationByCod,
    addFloraRescueZoneIdByName,
    addRescueFloraIdByNumber,
    addRelocationZoneIdByNumber
)

router = APIRouter()

# Upload flora rescue excel file
@router.post(
    path="/upload/flora_rescue",
    response_model= None,
    summary="Upload flora rescue excel file",
    tags=["Upload"],
)
async def upload_flora_rescue(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        # Convert date columns to datetime objects
        date_columns = ['rescue_date']
        df = convert_to_datetime(df, date_columns)

        #change coordinate system
        UTM_columns = {
            'easting': 'este',
            'northing': 'sur',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }

        #Names of columns geodata columns to in transect
        nameLatitude = 'latitude'
        nameLongitude = 'longitude'

        # Insert columns lat y lon to df
        df = insertGEOData(df, UTM_columns, nameLatitude, nameLongitude)

        #convert specie, genus and family bryophyte to id
        df, specieListWithOutNameB =  await addIdSpecieByName(db, df, "especie_forofito", "specie_bryophyte_id")
        df, genusListWithOutNameB = await addIdGenusByName(db, df, "genero_forofito", "genus_bryophyte_id")
        df, familyListWithOutNameB = await addIdFamilyByName(db, df, "familia_forofito", "family_bryophyte_id")

        #convert specie, genus and family epiphyte to id
        df, specieListWithOutNameE = await addIdSpecieByName(db, df, "especie_epifito", "specie_epiphyte_id")
        df, genusListWithOutNameE = await addIdGenusByName(db, df, "genero_epifito", "genus_epiphyte_id")
        df, familyListWithOutNameE = await addIdFamilyByName(db, df, "familia_epifito", "family_epiphyte_id")

        #convert rescue zone to id
        df, rescueZoneListWithOutName = await addFloraRescueZoneIdByName(db, df, "zona_rescate")

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_flora_rescue = FloraRescueBase(
                    epiphyte_number=row['number'],
                    rescue_date=row['rescue_date'],
                    rescue_area_latitude=row['latitude'],
                    rescue_area_longitude=row['longitude'],
                    substrate=none_value(row['sustrato_forofito']),
                    dap_bryophyte=none_value(row['DAP']),
                    height_bryophyte=none_value(row['altura_forofito']),
                    bryophyte_position=none_value(row['posicion_forofito']),
                    growth_habit=none_value(row['habito']),
                    epiphyte_phenology=none_value(row['fenologia_epifito']),
                    health_status_epiphyte=none_value(row['estado_sanitario_epifito']),
                    microhabitat=none_value(row['microhabitat']),
                    other_observations=none_value(row['observaciones']),
                    specie_bryophyte_id=none_value(row['specie_bryophyte_id']),
                    genus_bryophyte_id=none_value(row['genus_bryophyte_id']),
                    family_bryophyte_id=none_value(row['family_bryophyte_id']),
                    specie_epiphyte_id=none_value(row['specie_epiphyte_id']),
                    genus_epiphyte_id=none_value(row['genus_epiphyte_id']),
                    family_epiphyte_id=none_value(row['family_epiphyte_id']),
                    rescue_zone_id=row['idFloraRescueZone'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error in row {row['number']}: {e}"
                )
            if await get_flora_rescue(db, new_flora_rescue.epiphyte_number):
                numberExistList.append(new_flora_rescue.epiphyte_number)
                continue
            else:
                await create_flora_rescue(db, new_flora_rescue)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Flora rescue excel file uploaded successfully",
                "Numeros de epifitos ya existentes": numberExistList,
                "Especies forofito no encontradas": specieListWithOutNameB,
                "Generos forofito no encontrados": genusListWithOutNameB,
                "Familias forofito no encontradas": familyListWithOutNameB,
                "Especies epifito no encontradas": specieListWithOutNameE,
                "Generos epifito no encontrados": genusListWithOutNameE,
                "Familias epifito no encontradas": familyListWithOutNameE,
                "Zonas de rescate no encontradas": rescueZoneListWithOutName
                },
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

# Upload plant nursery excel file
@router.post(
    path="/upload/plant_nursery",
    response_model= None,
    summary="Upload plant nursery excel file",
    tags=["Upload"],
)
async def upload_plant_nursery(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Ensure sustrate is a string type
        df['tipo_sustrato'] = df['tipo_sustrato'].astype('Int64')
        df['tipo_sustrato'] = df['tipo_sustrato'].astype(str)

        # Ensure treatment_product is a string type
        df['producto_tratamiento'] = df['producto_tratamiento'].astype(str)

        # Replace NaN with None
        df = df.where(pd.notna(df), None)

        # Convert date columns to datetime objects
        date_columns = ['fecha_ingreso', 'fecha_floracion', 'fecha_salida']
        df = convert_to_datetime(df, date_columns)

        #add boolean column for is_phytosanitary_treatment and is_pruned
        df = addBooleanByCheck(df, "poda")
        df = addBooleanByCheck(df, "tratamiento_fitosanitario")

        #add id for flora rescue
        df, floraRescueListWithOutName = await addRescueFloraIdByNumber(db, df, "cod")

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_plant_nursery = PlantNurseryBase(
                    entry_date=row['fecha_ingreso'],
                    cod_reg=row['cod'],
                    health_status_epiphyte=none_value(row['estado_sanitario']),
                    vegetative_state=none_value(row['estado_vegetativo']),
                    flowering_date=none_value(row['fecha_floracion']),
                    treatment_product=none_value(row['producto_tratamiento']),
                    is_pruned=row['boolean_poda'],
                    is_phytosanitary_treatment=row['boolean_tratamiento_fitosanitario'],
                    substrate=none_value(row['tipo_sustrato']),
                    departure_date=none_value(row['fecha_salida']),
                    flora_rescue_id=row['idRescue'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error in row {row['cod']}: {e}"
                )
            if await get_plant_nursery(db, new_plant_nursery.cod_reg):
                numberExistList.append(new_plant_nursery.cod_reg)
                continue
            else:
                await create_plant_nursery(db, new_plant_nursery)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Plant nursery excel file uploaded successfully",
                "Codigos de registro ya existentes": numberExistList,
                "Codigos de rescate no encontrados": floraRescueListWithOutName
                },
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

# Upload flora relocation excel file
@router.post(
    path="/upload/flora_relocation",
    response_model= None,
    summary="Upload flora relocation excel file",
    tags=["Upload"],
)
async def upload_flora_relocation(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = df.where(pd.notna(df), None)

        # Convert date columns to datetime objects
        date_columns = ['fecha' ]
        df = convert_to_datetime(df, date_columns)

        #change coordinate system
        UTM_columns = {
            'easting': 'este',
            'northing': 'sur',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }

        #Names of columns geodata columns to in transect
        nameLatitude = 'latitude'
        nameLongitude = 'longitude'

        # Insert columns lat y lon to df
        df = insertGEOData(df, UTM_columns, nameLatitude, nameLongitude)

        #add id for flora rescue
        df, floraRescueListWithOutName = await addRescueFloraIdByNumber(db, df, "numer_rescue")


        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_flora_relocation = FloraRelocationBase(
                    relocation_date=row['fecha'],
                    relocation_number=row['number'],
                    size=row['tamaño'],
                    epiphyte_phenology=row['fenologia'],
                    johanson_zone=row['zona_johanson'],
                    relocation_position_latitude=row['latitude'],
                    relocation_position_longitude=row['longitude'],
                    relocation_position_altitude=row['altitud'],
                    bryophyte_number=row['numero_epifito'],
                    dap_bryophyte=row['dap'],
                    height_bryophyte=row['altura'],
                    bark_type=row['corteza'],
                    infested_lianas=row['lianas'],
                    other_observations=none_value(row['observaciones']),
                    flora_rescue_id=row['idRescue'],
                    specie_bryophyte_id=none_value(row['specie_bryophyte_id']),
                    genus_bryophyte_id=none_value(row['genus_bryophyte_id']),
                    family_bryophyte_id=none_value(row['family_bryophyte_id']),
                    relocation_zone_id=row['relocation_zone_id'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error in row {row['relocation_number']}: {e}"
                )
            if await get_flora_relocation(db, new_flora_relocation.relocation_number):
                numberExistList.append(new_flora_relocation.relocation_number)
                continue
            else:
                await create_flora_relocation(db, new_flora_relocation)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Flora relocation excel file uploaded successfully",
                "Codigos de registro ya existentes": numberExistList,
                "Codigos de rescate no encontrados": floraRescueListWithOutName
                },
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

#upload tower excel file
@router.post(
    path="/upload/tower",
    response_model= None,
    summary="Upload tower excel file",
    tags=["Upload"],
)
async def upload_tower(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_tower = TowerBase(
                    number=row['number'],
                    latitude=row['lat'],
                    longitude=row['lon'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error to create tower data: {e}",
                )
            if await get_tower_by_number(db, new_tower.number):
                numberExistList.append(new_tower.number)
                continue
            else:
                await create_tower(db, new_tower)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Tower excel file uploaded successfully", "numberExistList": numberExistList},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )


# Upload transect herpetofauna excel file
@router.post(
    path="/upload/transect_herpetofauna",
    summary="Upload transect herpetofauna excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_transect_herpetofauna(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse | HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        # Convert date columns to datetime objects
        date_columns = [
            'date_in',
            'date_out',
        ]

        # Convert UTM columns to GeoData
        UTM_columns_in = {
            'easting': 'este_in',
            'northing': 'sur_in',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }
        UTM_columns_out = {
            'easting': 'este_out',
            'northing': 'sur_out',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }

        #Names of columns geodata columns to in transect
        nameLatitude_in = 'latitude_in'
        nameLongitude_in = 'longitude_in'

        #Names of columns geodata columns to out transect
        nameLatitude_out = 'latitude_out'
        nameLongitude_out = 'longitude_out'

        # Insert columns lat y lon to df
        df = insertGEOData(df, UTM_columns_in, nameLatitude_in, nameLongitude_in)
        df = insertGEOData(df, UTM_columns_out, nameLatitude_out, nameLongitude_out)

        # Cnvert time to datetime
        df = convert_to_datetime(df, date_columns)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_transect_herpetofauna = TransectHerpetofaunaCreate(
                    number=row['num'],
                    date_in=row['date_in'],
                    date_out=row['date_out'],
                    latitude_in=row['latitude_in'],
                    longitude_in=row['longitude_in'],
                    altitude_in=row['altitud_in'],
                    latitude_out=row['latitude_out'],
                    longitude_out=row['longitude_out'],
                    altitude_out=row['altitud_out'],
                    tower_id=row['torre'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error: {e}",
                )
            if await get_transect_herpetofauna_by_number(db, new_transect_herpetofauna.number):
                numberExistList.append(new_transect_herpetofauna.number)
                continue
            else:
                await  create_transect_herpetofauna(db, new_transect_herpetofauna)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Flora relocation excel file uploaded successfully", "Not upload numbers because repeate": numberExistList},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

# Upload rescue herpetofauna excel file
@router.post(
    path="/upload/rescue_herpetofauna",
    summary="Upload rescue herpetofauna excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_rescue_herpetofauna(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse | HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        df, specieListWithOutName = await addIdSpecieByName(db, df, "especie", "idSpecie")
        df, genderListWithOutName = addBooleanByGender(df, "sexo",("Macho", "Hembra"))
        df, ageGroupListWithOutName = await addAgeGroupIdByName(db, df, "clase_etaria")
        df = await addTransectIdByNumber(db, df, "num_t")
        df = addNumRescueHerpeto(df, "num_t" )
        df = remplace_nan_with_none(df)

        numberExistList = []

        print(df)

        for _, row in df.iterrows():
            if row['idSpecie'] is None:
                continue
            else:
                try:
                    new_rescue_herpetofauna = RescueHerpetofaunaCreate(
                        number=row['numRescue'],
                        gender=none_value(row['booleanGender']),
                        specie_id=row['idSpecie'],
                        transect_herpetofauna_id=row['idTransect'],
                        age_group_id=none_value(row['idAgeGroup']),
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Error: {e} in row {row['numRescue']}",
                    )
                if await get_rescue_herpetofauna_by_number(db, new_rescue_herpetofauna.number):
                    numberExistList.append(new_rescue_herpetofauna.number)
                else:
                    await create_rescue_herpetofauna (db, new_rescue_herpetofauna)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "Flora relocation excel file uploaded successfully",
                "Not upload numbers because repeate": numberExistList,
                "Some species not found": specieListWithOutName,
                "Some gender not found or are null": genderListWithOutName,
                "Some age group not found or are null": ageGroupListWithOutName,
                },
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

# Upload mark herpetofauna excel file
@router.post(
    path="/upload/mark_herpetofauna",
    summary="Upload mark herpetofauna excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_mark_herpetofauna(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse | HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        # Convert date columns to datetime objects
        date_columns = [
            'date',
        ]
        df = convert_to_datetime(df, date_columns)
        df = addBooleanByCheck(df, "is_photo")
        df = addBooleanByCheck(df, "is_elastomer")
        df = await addRescueIdByNumber(db, df, "number_rescue")

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_mark_herpetofauna = MarkHerpetofaunaCreate(
                    date=row['date'],
                    number=row['number'],
                    code=row['cod'],
                    LHC=row['LHC'],
                    weight=row['peso'],
                    is_photo_mark=row['boolean_is_photo'],
                    is_elastomer_mark=row['boolean_is_elastomer'],
                    rescue_herpetofauna_id=row['idRescue'],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error: {e}",
                )
            if await get_mark_herpetofauna_by_number(db, new_mark_herpetofauna.number):
                numberExistList.append(new_mark_herpetofauna.number)
                continue
            else:
                await create_mark_herpetofauna(db, new_mark_herpetofauna)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "Flora relocation excel file uploaded successfully", "Not upload numbers because repeate": numberExistList},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

#Upload transect herpetofauna translocation
@router.post(
    path="/upload/transect_herpetofauna_translocation",
    summary="Upload transect herpetofauna translocation excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_transect_herpetofauna_translocation(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse|HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        # Convert date columns to datetime objects
        date_columns = [
            'date',
        ]
        df = convert_to_datetime(df, date_columns)

        #change coordinate system
        UTM_columns_in = {
            'easting': 'este_in',
            'northing': 'sur_in',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }
        UTM_columns_out = {
            'easting': 'este_out',
            'northing': 'sur_out',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }

        #Names of columns geodata columns to in transect
        nameLatitude_in = 'latitude_in'
        nameLongitude_in = 'longitude_in'

        #Names of columns geodata columns to out transect
        nameLatitude_out = 'latitude_out'
        nameLongitude_out = 'longitude_out'

        # Insert columns lat y lon to df
        df = insertGEOData(df, UTM_columns_in, nameLatitude_in, nameLongitude_in)
        df = insertGEOData(df, UTM_columns_out, nameLatitude_out, nameLongitude_out)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_transect_herpetofauna_translocation = TransectHerpetofaunaTranslocationCreate(
                    cod = row["cod"],
                    date = row["date"],
                    latitude_in= row["latitude_in"],
                    longitude_in= row["longitude_in"],
                    altitude_in= row["altitud_in"],
                    latitude_out= row["latitude_out"],
                    longitude_out= row["longitude_out"],
                    altitude_out= row["altitud_out"]
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error: {e}",
                )
            if await get_transect_herpetofauna_translocation_by_cod(db, new_transect_herpetofauna_translocation.cod):
                numberExistList.append(new_transect_herpetofauna_translocation.cod)
                continue
            else:
                await create_transect_herpetofauna_translocation(db, new_transect_herpetofauna_translocation)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "The file was upload", "Not upload numbers because repeate": numberExistList},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

#Upload point herpetofauna translocation
@router.post(
    path="/upload/point_herpetofauna_translocation",
    summary="Upload point herpetofauna translocation excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_point_herpetofaun_location(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse|HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        # Convert date columns to datetime objects
        date_columns = [
            'date',
        ]
        df = convert_to_datetime(df, date_columns)

        #change coordinate system
        UTM_columns = {
            'easting': 'este',
            'northing': 'sur',
            'zone_number': 'zona',
            'zone_letter': 'zona_letra',
        }

        #Names of columns geodata columns to in transect
        nameLatitude = 'latitude'
        nameLongitude = 'longitude'

        # Insert columns lat y lon to df
        df = insertGEOData(df, UTM_columns, nameLatitude, nameLongitude)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_point_herpetofauna_translocation = PointHerpetofaunaTranslocationCreate(
                    cod = row["cod"],
                    date = row["date"],
                    latitude= row["latitude"],
                    longitude= row["longitude"],
                    altitude= row["altitud"],
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error to create data: {e}",
                )
            if await get_point_herpetofauna_translocation_by_cod(db, new_point_herpetofauna_translocation.cod):
                numberExistList.append(new_point_herpetofauna_translocation.cod)
                continue
            else:
                await create_point_herpetofauna_translocation(db, new_point_herpetofauna_translocation)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "The file was upload", "Not upload numbers because repeate": numberExistList},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )

#Upload translocation herpetofauna
@router.post(
    path="/upload/translocation_herpetofauna",
    summary="Upload translocation herpetofauna excel file",
    response_model= None,
    tags=["Upload"],
)
async def upload_translocation_herpetofauna(
    file: UploadFile=File(...),
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> JSONResponse|HTTPException:
    if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
        df = pd.read_excel(file.file)

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        # Add id specie by scientific name
        df, specieListWithOutName = await addIdSpecieByName(db, df, "especie", "idSpecie")

        # Add id transect herpetofauna translocation by cod
        df = await addTransectTranslocationIdByCod(db, df, "cod_transect")

        # Add id point herpetofauna translocation by cod
        df = await addPointTranslocationByCod(db, df, "cod_point")

        # Add id mark herpetofauna by number
        df, markListWithOutNumber = await addMarkIdByNumber(db, df, "number_mark")

        # Replace NaN with None
        df = remplace_nan_with_none(df)

        numberExistList = []

        for _, row in df.iterrows():
            try:
                new_point_herpetofauna_translocation =  TranslocationHerpetofaunaCreate(
                    cod = row["cod"],
                    transect_herpetofauna_translocation_id = none_value(row["idTransect"]),
                    point_herpetofauna_translocation_id = none_value(row["idPoint"]),
                    specie_id = row["idSpecie"],
                    mark_herpetofauna_id=none_value(row["idMark"]),
                )
            except Exception as e:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Error to create data: {e} in row {row['cod']}",
                )
            if await get_translocation_herpetofauna_by_cod(db, new_point_herpetofauna_translocation.cod):
                numberExistList.append(new_point_herpetofauna_translocation.cod)
                continue
            else:
                await create_translocation_herpetofauna(db, new_point_herpetofauna_translocation)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "The file was upload", "Not upload numbers because repeate": numberExistList, "Some species not found": specieListWithOutName, "Some marks not found": markListWithOutNumber},
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an excel file",
        )






