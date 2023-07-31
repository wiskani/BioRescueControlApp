from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

import app.db.database as _database
import app.models.species


class Image(_database.Base):
    __tablename__ = 'images'
    id: Column [int]= Column(Integer, primary_key=True, index=True)
    atribute: Column [str]= Column(String, index=True, nullable=True)
    url: Column [str]= Column(String, index=True, nullable=True)
    created_at: Column [datetime]= Column(DateTime, default=datetime.utcnow)

    # Relationships with species
    species_id: Column [int]= Column(Integer, ForeignKey('species.id'))
    species = relationship("Specie", back_populates="images")

