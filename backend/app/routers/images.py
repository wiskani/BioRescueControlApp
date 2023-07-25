import os
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Union

from app.schemas.images import ImageBase, ImageResponse
from app.models.images import Image
from app.crud.images import get_image_by_url, create_image, get_all_images, get_image_by_id, update_image_by_id, delete_image_by_id
from app.api.deps import PermissonsChecker, get_db

router = APIRouter()

#create image
@router.post(
    path="/api/images_specie/",
    response_model=ImageResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["images"],
    summary="Create a image",
        )
async def create_image_specie(
    image: ImageBase,
    db: Session = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    db_image = get_image_by_url(db, image.url)
    if db_image:
        raise HTTPException(status_code=400, detail="Image already exists")
    return create_image(db, image)

#get all images
@router.get(
    path="/api/images_specie/",
    response_model=List[ImageResponse],
    tags=["images"],
    summary="Get all images",
)
async def get_all_images_specie(
    db: Session = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    return get_all_images(db)

#get image by id
@router.get(
    path="/api/images_specie/{image_id}",
    response_model=ImageResponse,
    tags=["images"],
    summary="Get image by id",
)
async def get_image_by_id_specie(
    image_id: int,
    db: Session = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
)-> Union[ImageResponse, HTTPException]:
    db_image = get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    return db_image

#update image by id
@router.put(
    path="/api/images_specie/{image_id}",
    response_model=ImageResponse,
    tags=["images"],
    summary="Update image by id",
)
async def update_image_by_id_specie(
    image_id: int,
    image: ImageBase,
    db: Session = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    return update_image_by_id(db, image_id, image)

#delete image by id
@router.delete(
    path="/api/images_specie/{image_id}",
    response_model=ImageResponse,
    tags=["images"],
    summary="Delete image by id",
)
async def delete_image_by_id_specie(
    image_id: int,
    db: Session = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    return delete_image_by_id(db, image_id)

#upload image
@router.post(
    path="/api/images_upload/{image_id}",
    summary="Upload image",
    tags=["images"],
)
async def upload_image(
    image_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    permissions: str = Depends(PermissonsChecker(["admin"])),
):
    db_image = get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    #check imagen foder
    images_folder ="static/images/species/"

    #check if folder exit
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    contents = await image.read()
    with open(f"static/images/species/{image.filename}", "wb") as f:
        f.write(contents)
    db_image.url = f"/static/images/species/{image.filename}"
    db.commit()
    db.refresh(db_image)
    return db_image




