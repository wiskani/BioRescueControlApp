from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

import app.models.towers
import app.db.database as _database
import app.models.species

class AgeGroup (_database.Base):
    __tablename__ = 'age_group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    #relationship with mark_herpetofauna
    mark_herpetofauna = relationship('MarkHerpetofauna', back_populates='age_group')


class TransectHerpetofauna (_database.Base):
    __tablename__ = 'transect_herpetofauna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    date_in: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    date_out: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    latitude_in: Mapped[float] = mapped_column(Float, nullable=False)
    longitude_in: Mapped[float] = mapped_column(Float, nullable=False)
    altitude_in: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude_out: Mapped[float] = mapped_column(Float, nullable=False)
    longitude_out: Mapped[float] = mapped_column(Float, nullable=False)
    altitude_out: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    #relationship with tower
    tower_id: Mapped[int] = mapped_column(Integer, ForeignKey('towers.id'))
    tower = relationship('Tower', back_populates='transect_herpetofauna')

    #relationship with rescue_herpetofauna
    rescue_herpetofauna = relationship('RescueHerpetofauna', back_populates='transect_herpetofauna')


class MarkHerpetofauna (_database.Base):
    __tablename__ = 'mark_herpetofauna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    gender: Mapped[bool] = mapped_column(Boolean, nullable=True)
    LHC : Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    is_photo_mark: Mapped[bool] = mapped_column(Boolean, default=False)
    is_elastomer_mark: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    #realtionship with age_group
    age_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('age_group.id'))
    age_group = relationship('AgeGroup', back_populates='mark_herpetofauna')

    #relationship with rescue_herpetofauna
    rescue_herpetofauna = relationship('RescueHerpetofauna', back_populates='mark_herpetofauna')

class RescueHerpetofauna (_database.Base):
    __tablename__ = 'rescue_herpetofauna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    #relationship with specie
    specie_id: Mapped[int] = mapped_column(Integer, ForeignKey('species.id'))
    specie = relationship('Specie', back_populates='rescue_herpetofauna')

    #relationship with mark_herpetofauna
    mark_herpetofauna_id: Mapped[int] = mapped_column(Integer, ForeignKey('mark_herpetofauna.id'))
    mark_herpetofauna = relationship('MarkHerpetofauna', back_populates='rescue_herpetofauna')

    #relationship with transect_herpetofauna
    transect_herpetofauna_id: Mapped[int] = mapped_column(Integer, ForeignKey('transect_herpetofauna.id'))
    transect_herpetofauna = relationship('TransectHerpetofauna', back_populates='rescue_herpetofauna')
