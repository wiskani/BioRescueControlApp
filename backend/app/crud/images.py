from sqlalchemy.orm import Session
from typing import List, Union
from fastapi import HTTPException

from app.models.images import Image
from app.schemas.images import ImageBase, ImageResponse

"""
PRUPPOSE: CRUD IMAGES
"""

#Get if image exists by url
def get_image_by_url(db: Session, url: str):
    return db.query(Image).filter(Image.url == url).first()

#Create a image
def create_image(db: Session, image: ImageBase) -> Image:
    db_image = Image(
        url=image.url,
        atribute=image.atribute,
        species_id=image.species_id
        )
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image

#Get all images
def get_all_images(db: Session) -> List[Image]:
    return db.query(Image).all()

#Get image by id
def get_image_by_id(db: Session, image_id: int) -> Image:
    return db.query(Image).filter(Image.id == image_id).first()

#Update image by id
def update_image_by_id(db: Session, image_id: int, image: ImageBase) -> Image:
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    db_image.url = image.url
    db_image.atribute = image.atribute
    db.commit()
    db.refresh(db_image)
    return db_image

#Delete image by id
def delete_image_by_id(db: Session, image_id: int) -> Image:
    db_image = db.query(Image).filter(Image.id == image_id).first()
    if not db_image:
        raise HTTPException(status_code=404, detail="Image not found")
    db.delete(db_image)
    db.commit()
    return db_image


