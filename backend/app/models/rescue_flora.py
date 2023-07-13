from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

import app.models.species
import app.db.database as _database

class FloraRescueZone(_database.Base):
    __tablename__ = "flora_rescue_zone"
    id:Column[int]= Column(Integer, primary_key=True, index=True)
    name: Column[str] = Column(String, index=True)
    description: Column[str] = Column(String, index=True)
    latitude: Column[float] = Column(Float, index=True)
    longitude: Column[float] = Column(Float, index=True)
    created_at: Column[datetime] = Column(DateTime, default=datetime.now())

    #Relationship for flora_rescue
    flora_rescue = relationship("FloraRescue", back_populates="flora_rescue_zone")

class FloraRescue(_database.Base):
    __tablename__ = "flora_rescue"
    id:Column[int]= Column(Integer, primary_key=True, index=True)
    epiphyte_number: Column[int] = Column(Integer, index=True)
    rescue_date: Column[datetime] = Column(DateTime)
    rescue_area_latitude: Column[float] = Column(Float, index=True)
    rescue_area_longitude: Column[float] = Column(Float, index=True)
    dap_bryophyte: Column[float] = Column(Float, index=True)
    height_bryophyte: Column[float] = Column(Float, index=True)
    bryophyte_position: Column[float] = Column(Float, index=True)
    growth_habit: Column[str] = Column(String, index=True)
    epiphyte_phenology: Column[str] = Column(String, index=True)
    health_status_epiphyte: Column[str] = Column(String, index=True)
    other_observations: Column[str] = Column(String, index=True)
    created_at: Column[datetime] = Column(DateTime, default=datetime.now())

    #Relationship for species
    specie_bryophyte_id: Column[int] = Column(Integer, ForeignKey("species.id"))
    specie_bryophyte = relationship("Specie", back_populates="flora_rescue_bryophyte")

    specie_epiphyte_id: Column[int] = Column(Integer, ForeignKey("species.id"))
    specie_epiphyte = relationship("Specie", back_populates="flora_rescue_epiphyte")

    # Relationships for flora_rescue_zone
    rescue_zone_id: Column[int] = Column(Integer, ForeignKey("flora_rescue_zone.id"))
    flora_rescue_zone = relationship("FloraRescueZone", back_populates="flora_rescue")

