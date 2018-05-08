from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from sqlalchemy import create_engine, MetaData, ForeignKey
from base import Base
from persons import Persons


engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)


class AddressToPerson(Base):
    __tablename__ = 'address_to_person'
    id = Column(Integer, primary_key = True)
    address = Column(String)
    person_id = Column(Integer, ForeignKey('persons.id'))


# create all tables
Base.metadata.create_all(engine)