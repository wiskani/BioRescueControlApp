from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

import app.db.database as _database
import app.models.images
import app.models.rescue_herpetofauna

class Status(_database.Base):
    __tablename__:str = "status"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    status_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships with specie
    species = relationship("Specie", back_populates="status")


class Specie(_database.Base):
    __tablename__:str = "species"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    scientific_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    specific_epithet: Mapped[str] = mapped_column(String, index=True)
    key_gbif: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships with status
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey("status.id"), nullable=True)
    status = relationship("Status", back_populates="species")

    # Relationships with genus
    genus_id: Mapped[int] = mapped_column(Integer, ForeignKey("genus.id"))
    genus = relationship("Genus", back_populates="species")

    # Relationships with flora_rescue
    flora_rescue_bryophyte = relationship("FloraRescue", back_populates="specie_bryophyte", foreign_keys="FloraRescue.specie_bryophyte_id")
    flora_rescue_epiphyte = relationship("FloraRescue", back_populates="specie_epiphyte", foreign_keys="FloraRescue.specie_epiphyte_id")

    # Relationships with flora_relocation
    flora_relocation_bryophyte = relationship("FloraRelocation", back_populates="specie_bryophyte")

    # Relationships with images
    images = relationship("Image", back_populates="species")

    # Relationships with rescue_herpetofauna
    rescue_herpetofauna = relationship("RescueHerpetofauna", back_populates="specie")

    # Relationships with translocation_herpetofauna
    translocation_herpetofauna = relationship("TranslocationHerpetofauna", back_populates="specie")

    # Relationships with rescue_mammals
    rescue_mammals = relationship("RescueMammals", back_populates="specie")



class Genus(_database.Base):
    __tablename__:str = "genus"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    genus_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    key_gbif: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships specie and family
    family_id: Mapped[int] = mapped_column(Integer, ForeignKey("family.id"))
    family = relationship("Family", back_populates="genus")
    species = relationship("Specie", back_populates="genus")

    # Relationships with flora_rescue
    flora_rescue_bryophyte = relationship("FloraRescue", back_populates="genus_bryophyte", foreign_keys="FloraRescue.genus_bryophyte_id")

    # Relationships with flora_relocation
    flora_relocation_bryophyte = relationship("FloraRelocation", back_populates="genus_bryophyte")



class Family(_database.Base):
    __tablename__:str = "family"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    family_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    key_gbif: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships order and genus
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"))
    order = relationship("Order", back_populates="family")
    genus = relationship("Genus", back_populates="family")

    # Relationships with flora_rescue
    flora_rescue_bryophyte = relationship("FloraRescue", back_populates="family_bryophyte", foreign_keys="FloraRescue.family_bryophyte_id")

    # Relationships with flora_relocation
    flora_relocation_bryophyte = relationship("FloraRelocation", back_populates="family_bryophyte")

class Order(_database.Base):
    __tablename__:str = "order"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    key_gbif: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    class__id: Mapped[int] = mapped_column(Integer, ForeignKey("class_.id"))
    class_ = relationship("Class_", back_populates="order")
    family = relationship("Family", back_populates="order")


class Class_(_database.Base):
    __tablename__:str = "class_"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    class_name: Mapped[str] = mapped_column(String, unique=True, index=True)
    key_gbif: Mapped[int] = mapped_column(Integer, unique=True, nullable=True)
    create_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    order = relationship("Order", back_populates="class_")
