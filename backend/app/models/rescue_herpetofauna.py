from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

import app.models.species
import app.db.database as _database

class AgeGroup (_database.Base):
    __tablename__ = 'age_group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    #relationship with rescue herpetofauna
    rescue_herpetofauna = relationship('RescueHerpetofauna', back_populates='age_group')


class RescueHerpetofauna (_database.Base):
    __tablename__ = 'rescue_herpetofauna'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    number: Mapped[int] = mapped_column(Integer, nullable=False)
    rescue_date_in: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    rescue_date_out: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    altitude: Mapped[int] = mapped_column(Integer, nullable=False)
    individual_count: Mapped[int] = mapped_column(Integer, nullable=True)
    gender: Mapped[bool] = mapped_column(Boolean, nullable=True)

    #relationship with age group
    age_group_id: Mapped[int] = mapped_column(Integer, ForeignKey('age_group.id'), nullable=True)
    age_group = relationship('AgeGroup', back_populates='rescue_herpetofauna')

    #relationship with species
    specie_id: Mapped[int] = mapped_column(Integer, ForeignKey('species.id'), nullable=True)
    species = relationship('Specie', back_populates='rescue_herpetofauna')


