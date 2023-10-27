from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from fastapi import HTTPException

from app.models.images import Image
from app.schemas.images import ImageBase

"""
PRUPPOSE: CRUD IMAGES
"""

#Get if image exists by url
async def get_image_by_url(db:AsyncSession , url: str) -> Image | None:
    image_db = await db.execute(select(Image).filter(Image.url == url))
    return image_db.scalars().first()

#Create a image
async def create_image(db:AsyncSession, image: ImageBase) -> Image:
    db_image = Image(
        url=image.url,
        atribute=image.atribute,
        species_id=image.species_id
        )
    db.add(db_image)
    await db.commit()
    await db.refresh(db_image)
    return db_image

#Get all images
async def get_all_images(db: AsyncSession ) -> List[Image]:
    images_db = await db.execute(select(Image))
    return list(images_db.scalars().all())

#Get image by id
async def get_image_by_id(db: AsyncSession, image_id: int) -> Image | None:
    image_db = await db.execute(select(Image).filter(Image.id == image_id))
    return image_db.scalars().first()

#Update image by id
async def update_image_by_id(db:AsyncSession , image_id: int, image: ImageBase) -> Image:
    db_image = await get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    db_image.url = image.url
    db_image.atribute = image.atribute
    await db.commit()
    await db.refresh(db_image)
    return db_image

#Delete image by id
async def delete_image_by_id(db: AsyncSession , image_id: int) -> Image:
    db_image = await get_image_by_id(db, image_id)
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    await db.execute(delete(Image).where(Image.id == image_id))
    await db.commit()
    return db_image


