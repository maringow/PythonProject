import os
import os.path
import re
from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from dateutil import parser
import email.utils
from sqlalchemy.orm.collections import attribute_mapped_collection


engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)
meta = MetaData()
Base = declarative_base(metadata=meta)


class Emails(Base):
    __tablename__ = 'emails2'
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
    x_filename = Column(String)

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
        x_filename = 'X-FileName'
    )
    key_by_label = {label:key for key, label in label_by_key.items()}


class Addresses(Base):
    __tablename__ = 'addresses2'
    id = Column(Integer, primary_key = True)
    email_id = Column(Integer, ForeignKey('emails2.id'), nullable = False)
    sent_datetime = Column(DateTime)
    sender = Column(String)
    send_type = Column(String)
    sent_to = Column(String)
    address_types = ['To', 'Cc', 'Bcc']
    key_by_address_type = {item:Emails.key_by_label[item] for item in address_types}


# create all tables
# Base.metadata.create_all(engine)


# read email and return sender and message ID
def parse_email(folder, filename):
    filename = os.path.join(folder, filename)
    body_pattern = r'(?s)^(.*?)\s?\n\s?\n(.*?)(?:\s?\n\s?\nMessage-ID.*)?$'
    header_pattern = r'(?s)(?:([\w-]+)[:]\s(.*?)\n)'
    # header_pattern = r'(?s)(?:([\w-]+)[:]\s*(.*?)\s?\n)'
    email = open(filename).read()
    try:
        header, body = re.findall(body_pattern, email)[0]
    except IndexError:
        return {}
    parsed_email = dict(re.findall(header_pattern, header))
    parsed_email['body'] = body
    return parsed_email

emails = []

for dirpath, dirnames, filenames in os.walk('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir\\lay-k'):
    for file in filenames:
        emails.append(parse_email(dirpath, file))

addresses = []
#
# for email in emails:
#     address = {}
#     email_id = # foreign key should populate this
#
#     sent_to_to = email['message_to'].split(',')
#     sent_to_cc = email['message_cc'].split(',')
#     sent_to_bcc = email['message_bcc'].split(',')
#
#     address['sent_datetime'] = email['sent_datetime']
#     address['sender'] = email['message_from']

# create database session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

key_errors = 0

for email in emails:
    try:
        kw = {Emails.key_by_label[label]:value for label, value in email.items()}
        dt = parser.parse(kw.pop('sent_datetime'))
        # print(kw)
    except KeyError as k:
        print('KeyError in message {}: {}'.format(email, k))
        key_errors += 1
    # add rows
    except ValueError as v:
        print('ValueError in message {}: {}'.format(email, v))
    try:
        emails_row = Emails(sent_datetime=dt, **kw)
        #session.add(emails_row)
        for address_type, column_name in Addresses.key_by_address_type.items():
            addresses = kw.get(column_name)
            if addresses:
                for address in addresses.split(','):
                    addresses_row = Addresses(sent_datetime=dt, sender=emails_row.message_from, send_type=address_type, sent_to=address.strip())
                    emails_row.addresses.append(addresses_row)
                # session.add(addresses_row)
        session.add(emails_row)
        session.commit()
        pass
        # if emails_row.message_to:
        #     addresses_row = Addresses(email_id = emails_row.id, sent_datetime=dt, sender=emails_row.message_from, send_type='To', sent_to=emails_row.message_to)
        #     session.add(addresses_row)
        # if emails_row.message_cc:
        #     addresses_row2 = Addresses(email_id = emails_row.id, sent_datetime=dt, sender=emails_row.message_from, send_type='Cc', sent_to=emails_row.message_cc)
        #     session.add(addresses_row2)
        # if emails_row.message_bcc:
        #     addresses_row3 = Addresses(email_id = emails_row.id, sent_datetime=dt, sender=emails_row.message_from, send_type='Bcc', sent_to=emails_row.message_bcc)
        #     session.add(addresses_row3)
    except SQLAlchemyError as e:
        print(e)
    finally:
        session.close()

print('Count of KeyErrors: {}'.format(key_errors))
