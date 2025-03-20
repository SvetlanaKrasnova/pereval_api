import enum
from datetime import datetime

from sqlalchemy import Column, Enum, Integer, TIMESTAMP, String, ForeignKey, Text, Float, LargeBinary
from sqlalchemy.orm import relationship
from .base import Base


class StatusEnum(enum.Enum):
    new = "new"
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Level(Base):
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    winter = Column(String(length=2), default='')
    summer = Column(String(length=2), default='')
    autumn = Column(String(length=2), default='')
    spring = Column(String(length=2), default='')
    pereval_added = relationship("PerevalAdded", back_populates="levels")


class User(Base):
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    email = Column(String(128), nullable=False, unique=True, index=True)
    fam = Column(String(150), nullable=False)
    name = Column(String(150), nullable=False)
    otc = Column(String(150), default='')
    phone = Column(String(15), unique=True)
    pereval_added = relationship("PerevalAdded", back_populates="user")


class Coord(Base):
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    height = Column(Integer, nullable=False)
    pereval_added = relationship("PerevalAdded", back_populates="coords")


class PerevalAdded(Base):
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    beauty_title = Column(String(250), nullable=False)
    title = Column(String(250), nullable=False)
    other_titles = Column(String(250), nullable=False)
    connect = Column(Text, default='')
    add_time = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    coord_id = Column(Integer, ForeignKey("coords.id"), nullable=False)
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)
    status = Column(Enum(StatusEnum), nullable=False, default="new")
    user = relationship("User", back_populates="pereval_added")
    coords = relationship("Coord", back_populates="pereval_added")
    levels = relationship("Level", back_populates="pereval_added")
    images = relationship("Image", back_populates="pereval")


class Image(Base):
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    data = Column(LargeBinary,  nullable=False)
    pereval_id = Column(Integer, ForeignKey("perevaladdeds.id"), nullable=False)
    pereval = relationship("PerevalAdded", back_populates="images")
