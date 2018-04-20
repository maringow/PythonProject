
from sqlalchemy import Column, Integer, String, Date, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
#from addresses import Addresses
from base import Base


class Emails(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key = True)
    message_id = Column(String)
    sent_datetime = Column(DateTime)
    message_from = Column(String)
    message_to = Column(String)
    message_cc = Column(String)
    message_bcc = Column(String)
    subject = Column(String)
    body = Column(String)
    mime_version = Column(Float)
    content_type = Column(String)
    content_transfer_encoding = Column(String)
    x_from = Column(String)
    x_to = Column(String)
    x_cc = Column(String)
    x_bcc = Column(String)
    x_folder = Column(String)
    x_origin = Column(String)
    filename = Column(String)
    duplicate_id = Column(Integer)

    addresses = relationship('Addresses', backref='email_ref') #, collection_class=attribute_mapped_collection('send_type'))

    label_by_key = dict(
        message_id = 'Message-ID',
        sent_datetime = 'Date',
        message_from = 'From',
        message_to = 'To',
        message_cc = 'Cc',
        message_bcc = 'Bcc',
        subject = 'Subject',
        body = 'body',
        mime_version = 'Mime-Version',
        content_type = 'Content-Type',
        content_transfer_encoding = 'Content-Transfer-Encoding',
        x_from = 'X-From',
        x_to = 'X-To',
        x_cc = 'X-cc',
        x_bcc = 'X-bcc',
        x_folder = 'X-Folder',
        x_origin = 'X-Origin',
        filename = 'filename'
    )
    key_by_label = {label:key for key, label in label_by_key.items()}

    @property  # like a calculated column in a report - allows you to reference as a member rather than as a function/method
    def duplicate_check(self):
        return self.body, self.message_to, self.sent_datetime

#
# class Addresses(Base):
#     __tablename__ = 'addresses'
#     id = Column(Integer, primary_key = True)
#     email_id = Column(Integer, ForeignKey('emails.id'), nullable = False)
#     sent_datetime = Column(DateTime)
#     sender = Column(String)
#     send_type = Column(String)
#     sent_to = Column(String)
#     address_types = ['To', 'Cc', 'Bcc']
#     key_by_address_type = {item:Emails.key_by_label[item] for item in address_types}