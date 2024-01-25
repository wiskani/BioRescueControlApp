import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status, Form, Body
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Annotated

from app.schemas.images import ImageBase, ImageResponse
from app.models.images import Image
from app.crud.images import get_image_by_url, create_image, get_all_images, get_image_by_id, update_image_by_id, delete_image_by_id
from app.api.deps import PermissonsChecker, get_db
from PIL import Image as PILImage
from io import BytesIO

router = APIRouter()


@router.post(
    path="/api/images_specie/",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["images"],
    summary="Create a image",
        )
async def create_image_specie(
    image: ImageBase,
    db:AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
):
    if not image.url:
        raise HTTPException(status_code=400, detail="Image url is required")
    db_image = await get_image_by_url(db, image.url)
    if db_image:
        raise HTTPException(status_code=400, detail="Image already exists")
    return await create_image(db, image)


@router.get(
    path="/api/images_specie/",
    response_model=List[ImageResponse],
    status_code=status.HTTP_200_OK,
    tags=["images"],
    summary="Get all images",
)
async def get_all_images_specie(
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin", "user"])),
) -> List[Image]:
    return await get_all_images(db)


@router.get(
    path="/api/images_specie/{image_id}",
    response_model=ImageResponse,
    tags=["images"],
    summary="Get image by id",
)
async def get_image_by_id_specie(
    image_id: int,
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
) -> Union[ImageResponse, HTTPException]:
    db_image = get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image


@router.put(
    path="/api/images_specie/{image_id}",
    response_model=ImageResponse,
    tags=["images"],
    summary="Update image by id",
)
async def update_image_by_id_specie(
    image_id: int,
    image: ImageBase,
    db: AsyncSession = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    return update_image_by_id(db, image_id, image)


@router.delete(
    path="/api/images_specie/{image_id}",
    response_model=ImageResponse,
    tags=["images"],
    summary="Delete image by id",
)
async def delete_image_by_id_specie(
    image_id: int,
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
):
    return delete_image_by_id(db, image_id)


@router.post(
    path="/api/image_upload",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload image",
    tags=["images"],
)
async def upload_image(
    image: Annotated[UploadFile, File(...)],
    specie_id: Annotated[int, Form(...)],
    atribute: Annotated[str, Form(...)],
    db: AsyncSession = Depends(get_db),
    authorized: bool = Depends(PermissonsChecker(["admin"])),
) -> Image:

    # check imagen foder
    images_folder = "static/images/species/"

    # check if folder exit
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    contents = await image.read()

    # Open image with PIL
    try:
        img = PILImage.open(BytesIO(contents))
        max_size = (640, 480)

        # Resize image
        img.thumbnail(max_size, PILImage.LANCZOS)

        # Save image
        img.save(os.path.join(images_folder, image.filename))

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        db_image = ImageBase(
                url=f"/static/images/species/{image.filename}",
                atribute=atribute,
                species_id=specie_id,
            )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if await get_image_by_url(db, f"/static/images/species/{image.filename}"):
        raise HTTPException(status_code=400, detail="Image already exists")
    return await create_image(db, db_image)




