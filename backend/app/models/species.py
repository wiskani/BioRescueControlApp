from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

import app.db.database as _database

class Specie(_database.Base):
    __tablename__:str = "species"
    id: Column = Column(Integer, primary_key=True, index=True)
    scientific_name: Column = Column(String, unique=True, index=True)
    common_name: Column = Column(String, unique=True, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)
    # Relationships
    genus_id: Column = Column(Integer, ForeignKey("genus.id"))
    genus = relationship("Genus", back_populates="species")

class Genus(_database.Base):
    __tablename__:str = "genus"
    id: Column = Column(Integer, primary_key=True, index=True)
    genus_name: Column = Column(String, unique=True, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    # Relationships
    species = relationship("Specie", back_populates="genus")

class Family(_database.Base):
    __tablename__:str = "family"
    id: Column = Column(Integer, primary_key=True, index=True)
    family_name: Column = Column(String, unique=True, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

class Order(_database.Base):
    __tablename__:str = "order"
    id: Column = Column(Integer, primary_key=True, index=True)
    order_name: Column = Column(String, unique=True, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

class Class(_database.Base):
    __tablename__:str = "class"
    id: Column = Column(Integer, primary_key=True, index=True)
    class_name: Column = Column(String, unique=True, index=True)
    create_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)
