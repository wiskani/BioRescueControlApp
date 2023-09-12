from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

import app.db.database as _database
import app.models.species


class Image(_database.Base):
    __tablename__ = 'images'
    id: Mapped [int]= mapped_column(Integer, primary_key=True, index=True)
    atribute: Mapped [str]= mapped_column(String, index=True, nullable=True)
    url: Mapped [str]= mapped_column(String, index=True, nullable=True)
    created_at: Mapped [datetime]= mapped_column(DateTime, default=datetime.utcnow)

    # Relationships with species
    species_id: Mapped [int]= mapped_column(Integer, ForeignKey('species.id'))
    species = relationship("Specie", back_populates="images")

