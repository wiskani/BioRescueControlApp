from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

import app.models.species
import app.db.database as _database

class FloraRescueZone(_database.Base):
    __tablename__ = "flora_rescue_zone"
    id:Column[int]= Column(Integer, primary_key=True, index=True)
    name: Column[str] = Column(String, index=True)
    description: Column[str] = Column(String, index=True)
    created_at: Column[datetime] = Column(DateTime, default=datetime.now())

    #Relationship for flora_rescue
    flora_rescue = relationship("FloraRescue", back_populates="flora_rescue_zone")

    #Relationship for plant_nursery
    plant_nursery = relationship("PlantNursery", back_populates="flora_rescue_zone")

    #Relationship for flora_relocation
    flora_relocation = relationship("FloraRelocation", back_populates="flora_rescue_zone")

class FloraRelocationZone(_database.Base):
    __tablename__ = "flora_relocation_zone"
    id:Column[int]= Column(Integer, primary_key=True, index=True)
    name: Column[str] = Column(String, index=True)
    created_at: Column[datetime] = Column(DateTime, default=datetime.now())

    #Relationship for plant_nursery
    plant_nursery = relationship("PlantNursery", back_populates="flora_relocation_zone")

    #Relationship for flora_relocation
    flora_relocation = relationship("FloraRelocation", back_populates="flora_relocation_zone")


class FloraRescue(_database.Base):
    __tablename__ = "flora_rescue"
    id:Column[int]= Column(Integer, primary_key=True, index=True)
    epiphyte_number: Column[int] = Column(Integer, index=True)
    rescue_date: Column[datetime] = Column(DateTime)
    rescue_area_latitude: Column[float] = Column(Float, index=True)
    rescue_area_longitude: Column[float] = Column(Float, index=True)
    substrate: Column[str] = Column(String, index=True, nullable=True)
    dap_bryophyte: Column[float] = Column(Float, index=True, nullable=True)
    height_bryophyte: Column[float] = Column(Float, index=True, nullable=True)
    bryophyte_position: Column[int] = Column(Integer, index=True, nullable=True)
    growth_habit: Column[str] = Column(String, index=True)
    epiphyte_phenology: Column[str] = Column(String, index=True)
    health_status_epiphyte: Column[str] = Column(String, index=True)
    microhabitat: Column[str] = Column(String, index=True)
    other_observations: Column[str] = Column(String, index=True)
    created_at: Column[datetime] = Column(DateTime, default=datetime.now())

    #Relationship for species
    specie_bryophyte_id: Column[int] = Column(Integer, ForeignKey("species.id"), nullable=True)
    specie_bryophyte = relationship("Specie", back_populates="flora_rescue_bryophyte", foreign_keys=[specie_bryophyte_id])

    specie_epiphyte_id: Column[int] = Column(Integer, ForeignKey("species.id"))
    specie_epiphyte = relationship("Specie", back_populates="flora_rescue_epiphyte", foreign_keys=[specie_epiphyte_id])

    #Relationship for genus
    genus_bryophyte_id: Column[int] = Column(Integer, ForeignKey("genus.id"), nullable=True)
    genus_bryophyte = relationship("Genus", back_populates="flora_rescue_bryophyte", foreign_keys=[genus_bryophyte_id])

    #Relationship for family
    family_bryophyte_id: Column[int] = Column(Integer, ForeignKey("family.id"), nullable=True)
    family_bryophyte = relationship("Family", back_populates="flora_rescue_bryophyte", foreign_keys=[family_bryophyte_id])

    # Relationships for flora_rescue_zone
    rescue_zone_id: Column[int] = Column(Integer, ForeignKey("flora_rescue_zone.id"))
    flora_rescue_zone = relationship("FloraRescueZone", back_populates="flora_rescue")

    # Relationships for plant_nursery
    plant_nursery = relationship("PlantNursery", uselist=False, back_populates="flora_rescue")

    # Relationships for flora_relocation
    flora_relocation = relationship("FloraRelocation", uselist=False, back_populates="flora_rescue")


class PlantNursery(_database.Base):
    __tablename__ = "plant_nursery"
    id:Column[int]= Column(Integer, primary_key=True, index=True)
    entry_date: Column[datetime] = Column(DateTime)
    cod_reg: Column[str] = Column(String, index=True)
    health_status_epiphyte: Column[str] = Column(String, index=True)
    vegetative_state: Column[str] = Column(String, index=True)
    flowering_date: Column[datetime] = Column(DateTime)
    treatment_product: Column[str] = Column(String, index=True)
    is_pruned: Column[bool] = Column(Boolean, default=False)
    is_phytosanitary_treatment: Column[bool] = Column(Boolean, default=False)
    substrate: Column[str] = Column(String, index=True)
    departure_date: Column[datetime] = Column(DateTime)
    created_at: Column[datetime] = Column(DateTime, default=datetime.now())

    #Relationship for flora_rescue_zone
    rescue_zone_id: Column[int] = Column(Integer, ForeignKey("flora_rescue_zone.id"))
    flora_rescue_zone = relationship("FloraRescueZone", back_populates="plant_nursery")

    #Relationship for flora_rescue
    flora_rescue_id: Column[int] = Column(Integer, ForeignKey("flora_rescue.id"))
    flora_rescue = relationship("FloraRescue", back_populates="plant_nursery")

    #Relationship for species
    specie_id: Column[int] = Column(Integer, ForeignKey("species.id"))
    specie = relationship("Specie", back_populates="plant_nursery")

    #Relationship for flora_relocation_zone
    relocation_zone_id: Column[int] = Column(Integer, ForeignKey("flora_relocation_zone.id"))
    flora_relocation_zone = relationship("FloraRelocationZone", back_populates="plant_nursery")

class FloraRelocation(_database.Base):
    __tablename__ = "flora_relocation"
    id:Column[int]= Column(Integer, primary_key=True, index=True)
    relocation_date: Column[datetime] = Column(DateTime)
    size: Column[float] = Column(Float, index=True)
    epiphyte_phenology: Column[str] = Column(String, index=True)
    johanson_zone: Column[str] = Column(String, index=True)
    relocation_position_latitude: Column[float] = Column(Float, index=True)
    relocation_position_longitude: Column[float] = Column(Float, index=True)
    bryophyte_number: Column[int] = Column(Integer, index=True)
    dap_bryophyte: Column[float] = Column(Float, index=True)
    height_bryophyte: Column[float] = Column(Float, index=True)
    bryophyte_position: Column[int] = Column(Integer, index=True)
    bark_type: Column[str] = Column(String, index=True)
    infested_lianas: Column[str] = Column(String, index=True)
    relocation_number: Column[int] = Column(Integer, index=True)
    other_observations: Column[str] = Column(String, index=True)
    created_at: Column[datetime] = Column(DateTime, default=datetime.now())

    #Relationship for rescue_zone 
    rescue_zone_id: Column[int] = Column(Integer, ForeignKey("flora_rescue_zone.id"))
    flora_rescue_zone = relationship("FloraRescueZone", back_populates="flora_relocation")

    #Relationship for flora rescue
    flora_rescue_id: Column[int] = Column(Integer, ForeignKey("flora_rescue.id"))
    flora_rescue = relationship("FloraRescue", back_populates="flora_relocation")

    #Relationship for species
    specie_bryophyte_id: Column[int] = Column(Integer, ForeignKey("species.id"))
    specie_bryophyte = relationship("Specie", back_populates="flora_relocation_bryophyte")

    #Relationship for flora_relocation_zone
    relocation_zone_id: Column[int] = Column(Integer, ForeignKey("flora_relocation_zone.id"))
    flora_relocation_zone = relationship("FloraRelocationZone", back_populates="flora_relocation")



