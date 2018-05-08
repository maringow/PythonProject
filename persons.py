from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from base import Base


class Persons(Base):
    __tablename__ = 'persons'
    id = Column(Integer, primary_key = True)
    name = Column(String)

