from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

import pytz
import app.models.species
import app.db.database as _database

class FloraRescueZone(_database.Base):
    __tablename__ = "flora_rescue_zone"
    id:Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/La_Paz')))

    #Relationship for flora_rescue
    flora_rescue = relationship("FloraRescue", back_populates="flora_rescue_zone")


class FloraRelocationZone(_database.Base):
    __tablename__ = "flora_relocation_zone"
    id:Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/La_Paz')))

    #Relationship for flora_relocation
    flora_relocation = relationship("FloraRelocation", back_populates="flora_relocation_zone")



class FloraRescue(_database.Base):
    __tablename__ = "flora_rescue"
    id:Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    epiphyte_number: Mapped[str] = mapped_column(String, index=True, unique=True)
    rescue_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    rescue_area_latitude: Mapped[float] = mapped_column(Float, index=True)
    rescue_area_longitude: Mapped[float] = mapped_column(Float, index=True)
    substrate: Mapped[str] = mapped_column(String, index=True, nullable=True)
    dap_bryophyte: Mapped[float] = mapped_column(Float, index=True, nullable=True)
    height_bryophyte: Mapped[float] = mapped_column(Float, index=True, nullable=True)
    bryophyte_position: Mapped[int] = mapped_column(Integer, index=True, nullable=True)
    growth_habit: Mapped[str] = mapped_column(String, index=True, nullable=True)
    epiphyte_phenology: Mapped[str] = mapped_column(String, index=True, nullable=True)
    health_status_epiphyte: Mapped[str] = mapped_column(String, index=True, nullable=True)
    microhabitat: Mapped[str] = mapped_column(String, index=True, nullable=True)
    other_observations: Mapped[str] = mapped_column(String, nullable=True) 
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/La_Paz')))

    #Relationship for species
    specie_bryophyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("species.id"), nullable=True)
    specie_bryophyte = relationship("Specie", back_populates="flora_rescue_bryophyte", foreign_keys=[specie_bryophyte_id])

    specie_epiphyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("species.id"), nullable=True)
    specie_epiphyte = relationship("Specie", back_populates="flora_rescue_epiphyte", foreign_keys=[specie_epiphyte_id])

    #Relationship for genus
    genus_bryophyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("genus.id"), nullable=True)
    genus_bryophyte = relationship("Genus", back_populates="flora_rescue_bryophyte", foreign_keys=[genus_bryophyte_id])

    genus_epiphyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("genus.id"), nullable=True)
    genus_epiphyte = relationship("Genus", back_populates="flora_rescue_epiphyte", foreign_keys=[genus_epiphyte_id])

    #Relationship for family
    family_bryophyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("family.id"), nullable=True)
    family_bryophyte = relationship("Family", back_populates="flora_rescue_bryophyte", foreign_keys=[family_bryophyte_id])

    family_epiphyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("family.id"), nullable=True)
    family_epiphyte = relationship("Family", back_populates="flora_rescue_epiphyte", foreign_keys=[family_epiphyte_id])

    # Relationships for flora_rescue_zone
    rescue_zone_id: Mapped[int] = mapped_column(Integer, ForeignKey("flora_rescue_zone.id"))
    flora_rescue_zone = relationship("FloraRescueZone", back_populates="flora_rescue")

    # Relationships for plant_nursery
    plant_nursery = relationship("PlantNursery", uselist=False, back_populates="flora_rescue")

    # Relationships for flora_relocation
    flora_relocation = relationship("FloraRelocation", uselist=False, back_populates="flora_rescue")


class PlantNursery(_database.Base):
    __tablename__ = "plant_nursery"
    id:Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    entry_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    cod_reg: Mapped[str] = mapped_column(String, index=True)
    health_status_epiphyte: Mapped[str] = mapped_column(String, index=True, nullable=True)
    vegetative_state: Mapped[str] = mapped_column(String, index=True, nullable=True)
    flowering_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    treatment_product: Mapped[str] = mapped_column(String, index=True, nullable=True)
    is_pruned: Mapped[bool] = mapped_column(Boolean, default=False)
    is_phytosanitary_treatment: Mapped[bool] = mapped_column(Boolean, default=False)
    substrate: Mapped[str] = mapped_column(String, index=True, nullable=True)
    departure_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/La_Paz')))

    #Relationship for flora_rescue
    flora_rescue_id: Mapped[int] = mapped_column(Integer, ForeignKey("flora_rescue.id"))
    flora_rescue = relationship("FloraRescue", back_populates="plant_nursery")


class FloraRelocation(_database.Base):
    __tablename__ = "flora_relocation"
    id:Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    relocation_date: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    size: Mapped[float] = mapped_column(Float, index=True)
    epiphyte_phenology: Mapped[str] = mapped_column(String, index=True)
    johanson_zone: Mapped[str] = mapped_column(String, index=True, nullable=True)
    relocation_position_latitude: Mapped[float] = mapped_column(Float, index=True)
    relocation_position_longitude: Mapped[float] = mapped_column(Float, index=True)
    bryophyte_number: Mapped[int] = mapped_column(Integer, index=True)
    dap_bryophyte: Mapped[float] = mapped_column(Float, index=True, nullable=True)
    height_bryophyte: Mapped[float] = mapped_column(Float, index=True, nullable=True)
    bark_type: Mapped[str] = mapped_column(String, index=True, nullable=True)
    infested_lianas: Mapped[str] = mapped_column(String, index=True, nullable=True)
    relocation_number: Mapped[int] = mapped_column(Integer, index=True, nullable=True)
    other_observations: Mapped[str] = mapped_column(String, index=True, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now(pytz.timezone('America/La_Paz')))

    #Relationship for flora rescue
    flora_rescue_id: Mapped[int] = mapped_column(Integer, ForeignKey("flora_rescue.id"))
    flora_rescue = relationship("FloraRescue", back_populates="flora_relocation")

    #Relationship for species bryophyte
    specie_bryophyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("species.id"), nullable=True)
    specie_bryophyte = relationship("Specie", back_populates="flora_relocation_bryophyte")

    #Relationship for genus bryophyte
    genus_bryophyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("genus.id"), nullable=True)
    genus_bryophyte = relationship("Genus", back_populates="flora_relocation_bryophyte")

    #Relationship for family bryophyte
    family_bryophyte_id: Mapped[int] = mapped_column(Integer, ForeignKey("family.id"), nullable=True)
    family_bryophyte = relationship("Family", back_populates="flora_relocation_bryophyte")


    #Relationship for flora_relocation_zone
    relocation_zone_id: Mapped[int] = mapped_column(Integer, ForeignKey("flora_relocation_zone.id"))
    flora_relocation_zone = relationship("FloraRelocationZone", back_populates="flora_relocation")



