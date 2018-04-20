from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from base import Base
from emails import Emails


class Addresses(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key = True)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable = False)
    sent_datetime = Column(DateTime)
    sender = Column(String)
    send_type = Column(String)
    sent_to = Column(String)
    address_types = ['To', 'Cc', 'Bcc']
    key_by_address_type = {item:Emails.key_by_label[item] for item in address_types}