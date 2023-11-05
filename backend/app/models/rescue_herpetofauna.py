from sqlalchemy import Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

import pytz
import app.models.towers
import app.db.database as _database
import app.models.species

class AgeGroup (_database.Base):
    __tablename__ = 'age_group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with rescue_herpetofauna
    rescue_herpetofauna = relationship('RescueHerpetofauna', back_populates='age_group')


class TransectHerpetofauna (_database.Base):
    __tablename__ = 'transect_herpetofauna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    date_in: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    date_out: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    latitude_in: Mapped[float] = mapped_column(Float, nullable=False)
    longitude_in: Mapped[float] = mapped_column(Float, nullable=False)
    altitude_in: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude_out: Mapped[float] = mapped_column(Float, nullable=False)
    longitude_out: Mapped[float] = mapped_column(Float, nullable=False)
    altitude_out: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with tower
    tower_id: Mapped[int] = mapped_column(Integer, ForeignKey('towers.id'))
    tower = relationship('Tower', back_populates='transect_herpetofauna')

    #relationship with rescue_herpetofauna
    rescue_herpetofauna = relationship('RescueHerpetofauna', back_populates='transect_herpetofauna')


class MarkHerpetofauna (_database.Base):
    __tablename__ = 'mark_herpetofauna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    number: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)
    code: Mapped[str] = mapped_column(String(50), nullable=True, unique=False)
    LHC : Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    is_photo_mark: Mapped[bool] = mapped_column(Boolean, default=False)
    is_elastomer_mark: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False,default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with rescue_herpetofauna
    rescue_herpetofauna_id: Mapped[int] = mapped_column(Integer, ForeignKey('rescue_herpetofauna.id'))
    rescue_herpetofauna = relationship('RescueHerpetofauna', back_populates='mark_herpetofauna')

class RescueHerpetofauna (_database.Base):
    __tablename__ = 'rescue_herpetofauna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[str] = mapped_column(String, nullable=False)
    gender: Mapped[bool] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with specie
    specie_id: Mapped[int] = mapped_column(Integer, ForeignKey('species.id'))
    specie = relationship('Specie', back_populates='rescue_herpetofauna')

    #relationship with mark_herpetofauna
    mark_herpetofauna = relationship('MarkHerpetofauna', back_populates='rescue_herpetofauna')


    #relationship with transect_herpetofauna
    transect_herpetofauna_id: Mapped[int] = mapped_column(Integer, ForeignKey('transect_herpetofauna.id'))
    transect_herpetofauna = relationship('TransectHerpetofauna', back_populates='rescue_herpetofauna')

    #relationship with age_group
    age_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('age_group.id'), nullable=True)
    age_group = relationship('AgeGroup', back_populates='rescue_herpetofauna')


class TransectHerpetofaunaTranslocation (_database.Base):
    __tablename__ = 'transect_herpetofauna_translocation'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cod: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    latitude_in: Mapped[float] = mapped_column(Float, nullable=False)
    longitude_in: Mapped[float] = mapped_column(Float, nullable=False)
    altitude_in: Mapped[int] = mapped_column(Integer, nullable=False)
    latitude_out: Mapped[float] = mapped_column(Float, nullable=False)
    longitude_out: Mapped[float] = mapped_column(Float, nullable=False)
    altitude_out: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with translocation_herpetofauna
    translocation_herpetofauna = relationship('TranslocationHerpetofauna', back_populates='transect_herpetofauna_translocation')


class PointHerpetofaunaTranslocation (_database.Base):
    __tablename__ = 'point_herpetofauna_translocation'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cod: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    altitude: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with translocation_herpetofauna
    translocation_herpetofauna = relationship('TranslocationHerpetofauna', back_populates='point_herpetofauna_translocation')

class TranslocationHerpetofauna (_database.Base):
    __tablename__ = 'translocation_herpetofauna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cod: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with transect_herpetofauna_translocation
    transect_herpetofauna_translocation_id: Mapped[int] = mapped_column(Integer, ForeignKey('transect_herpetofauna_translocation.id'), nullable=True)
    transect_herpetofauna_translocation = relationship('TransectHerpetofaunaTranslocation', back_populates='translocation_herpetofauna')

    #relationship with point_rescue_herpetofauna_translocation
    point_herpetofauna_translocation_id: Mapped[int] = mapped_column(Integer, ForeignKey('point_herpetofauna_translocation.id'), nullable=True)
    point_herpetofauna_translocation = relationship('PointHerpetofaunaTranslocation', back_populates='translocation_herpetofauna')

    #relationship with specie
    specie_id: Mapped[int] = mapped_column(Integer, ForeignKey('species.id'))
    specie = relationship('Specie', back_populates='translocation_herpetofauna')


