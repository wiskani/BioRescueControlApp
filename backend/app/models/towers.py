from sqlalchemy import Column, Integer, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

import app.db.database as _database

class Tower(_database.Base):
    __tablename__:str = "towers"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    number: Column[int] = Column(Integer, unique=True)
    latitude: Column[float] = Column(Float, index=True)
    longitude: Column[float] = Column(Float, index=True)
    created_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    #relationship with clear_flora
    clear_flora = relationship("Clear_flora", back_populates="tower")

    #relationship with clear_herpetofauna
    clear_herpetofauna = relationship("Clear_herpetofauna", back_populates="tower")

    #relationship with clear_mammals
    clear_mammals = relationship("Clear_mammals", back_populates="tower")

class Clear_flora(_database.Base):
    __tablename__:str = "clear_flora"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    is_clear: Column[bool] = Column(Boolean, default=False)
    tower_id: Column[int] = Column(Integer, ForeignKey("towers.id"), unique=True)
    clear_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)
    created_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    #relationship with tower
    tower = relationship("Tower", back_populates="clear_flora")

class Clear_herpetofauna(_database.Base):
    __tablename__:str = "clear_herpetofauna"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    is_clear: Column[bool] = Column(Boolean, default=False)
    tower_id: Column[int] = Column(Integer, ForeignKey("towers.id"), unique=True)
    clear_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)
    created_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    #relationship with tower
    tower = relationship("Tower", back_populates="clear_herpetofauna")

class Clear_mammals(_database.Base):
    __tablename__:str = "clear_mammals"
    id: Column[int] = Column(Integer, primary_key=True, index=True)
    is_clear: Column[bool] = Column(Boolean, default=False)
    tower_id: Column[int] = Column(Integer, ForeignKey("towers.id"), unique=True)
    clear_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)
    created_at: Column[datetime] = Column(DateTime, default=datetime.utcnow)

    #relationship with tower
    tower = relationship("Tower", back_populates="clear_mammals")
