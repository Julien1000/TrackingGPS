from sqlalchemy import Column, Integer, Float, String, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "user"
    nom = Column(String(20), primary_key=True)

class Coord(Base):
    __tablename__ = "coord"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom = Column(String(20), ForeignKey("user.nom"), nullable=False)
    longitude = Column(Float, nullable=False)
    latitude = Column(Float, nullable=False)
    date1 = Column(TIMESTAMP, nullable=False)
