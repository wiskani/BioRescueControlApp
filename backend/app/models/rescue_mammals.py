from sqlalchemy import Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

import pytz
import app.models.towers
import app.models.rescue_herpetofauna
import app.db.database as _database
import app.models.species

class Habitat(_database.Base):
    __tablename__ = 'habitat'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with rescue_mammals
    rescue_mammals = relationship('RescueMammals', back_populates='habitat')

class RescueMammals(_database.Base):
    __tablename__ = 'rescue_mammals'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cod: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    mark: Mapped[str] = mapped_column(String(150), nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    altitude: Mapped[int] = mapped_column(Integer, nullable=False)
    gender: Mapped[bool] = mapped_column(Boolean, nullable=True)
    LT: Mapped[float] = mapped_column(Float, nullable=True)
    LC: Mapped[float] = mapped_column(Float, nullable=True)
    LP: Mapped[float] = mapped_column(Float, nullable=True)
    LO: Mapped[float] = mapped_column(Float, nullable=True)
    LA: Mapped[float] = mapped_column(Float, nullable=True)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    observation: Mapped[str] = mapped_column(String(200), nullable=True)
    is_specie_confirmed: Mapped[bool] = mapped_column(Boolean, nullable=False)
    create_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with habitat
    habitat_id: Mapped[int] = mapped_column(Integer, ForeignKey('habitat.id'))
    habitat = relationship('Habitat', back_populates='rescue_mammals')

    #relationship with age_group
    age_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('age_group.id'), nullable=True)
    age_group = relationship('AgeGroup', back_populates='rescue_mammals')

    #relationship with species
    specie_id: Mapped[int] = mapped_column(Integer, ForeignKey('species.id'), nullable=True)
    specie = relationship('Specie', back_populates='rescue_mammals')

    #relationship with genus
    genus_id: Mapped[int] = mapped_column(Integer, ForeignKey('genus.id'), nullable=True)
    genus = relationship('Genus', back_populates='rescue_mammals')

    #relationship with release_mammals
    release_mammals = relationship('ReleaseMammals', back_populates='rescue_mammals')


class SiteReleaseMammals(_database.Base):
    __tablename__ = 'site_release_mammals'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now(pytz.timezone('America/La_Paz')))

    #relationship with release_mammals
    release_mammals = relationship('ReleaseMammals', back_populates='site_release_mammals')

class ReleaseMammals(_database.Base):
    __tablename__ = 'release_mammals'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    cod: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=True)
    altitude: Mapped[int] = mapped_column(Integer, nullable=True)
    sustrate: Mapped[str] = mapped_column(String(50), nullable=True)

    #relationship with site_release_mammals
    site_release_mammals_id: Mapped[int] = mapped_column(Integer, ForeignKey('site_release_mammals.id'))
    site_release_mammals = relationship('SiteReleaseMammals', back_populates='release_mammals')

    #relationship with rescue_mammals
    rescue_mammals_id: Mapped[int] = mapped_column(Integer, ForeignKey('rescue_mammals.id'))
    rescue_mammals = relationship('RescueMammals', back_populates='release_mammals')




