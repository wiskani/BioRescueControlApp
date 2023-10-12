from sqlalchemy import Integer, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime

import app.db.database as _database

class Tower(_database.Base):
    __tablename__:str = "towers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, unique=True)
    latitude: Mapped[float] = mapped_column(Float, index=True)
    longitude: Mapped[float] = mapped_column(Float, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    #relationship with clear_flora
    clear_flora = relationship("Clear_flora", back_populates="tower")

    #relationship with clear_herpetofauna
    clear_herpetofauna = relationship("Clear_herpetofauna", back_populates="tower")

    #relationship with clear_mammals
    clear_mammals = relationship("Clear_mammals", back_populates="tower")

    #relationship with rescue_herpetofauna
    rescue_herpetofauna = relationship("Rescue_herpetofauna", back_populates="tower")

class Clear_flora(_database.Base):
    __tablename__:str = "clear_flora"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    is_clear: Mapped[bool] = mapped_column(Boolean, default=False)
    tower_id: Mapped[int] = mapped_column(Integer, ForeignKey("towers.id"), unique=True)
    clear_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    #relationship with tower
    tower = relationship("Tower", back_populates="clear_flora")

class Clear_herpetofauna(_database.Base):
    __tablename__:str = "clear_herpetofauna"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    is_clear: Mapped[bool] = mapped_column(Boolean, default=False)
    tower_id: Mapped[int] = mapped_column(Integer, ForeignKey("towers.id"), unique=True)
    clear_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    #relationship with tower
    tower = relationship("Tower", back_populates="clear_herpetofauna")

class Clear_mammals(_database.Base):
    __tablename__:str = "clear_mammals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    is_clear: Mapped[bool] = mapped_column(Boolean, default=False)
    tower_id: Mapped[int] = mapped_column(Integer, ForeignKey("towers.id"), unique=True)
    clear_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    #relationship with tower
    tower = relationship("Tower", back_populates="clear_mammals")
