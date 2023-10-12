from sqlalchemy import Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime

import app.models.species
import app.models.towers
import app.db.database as _database

class AgeGroup (_database.Base):
    __tablename__ = 'age_group'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)


class TransectHerpetofauna (_database.Base):
    __tablename__ = 'rescue_herpetofauna'
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

    #relationship with tower
    tower_id: Mapped[int] = mapped_column(Integer, ForeignKey('tower.id'))
    tower = relationship('Tower', back_populates='rescue_herpetofauna')


