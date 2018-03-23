import os
import os.path
import re
from sqlalchemy import create_engine, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dateutil import parser


engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)
meta = MetaData()
Base = declarative_base(metadata=meta)


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
    x_filename = Column(String)
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
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key = True)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable = False)
    sender = Column(String, ForeignKey('emails.message_from'))
    send_type = Column(String)
    sent_to = Column(String)


# read email and return sender and message ID
def parse_email(folder, filename):
    filename = os.path.join(folder, filename)
    body_pattern = r'(?s)^(.*?)\s?\n\s?\n(.*?)(?:\s?\n\s?\nMessage-ID.*)?$'
    header_pattern = r'(?s)(?:([\w-]+)[:]\s(.*?)\n)'
    # header_pattern = r'(?s)(?:([\w-]+)[:]\s*(.*?)\s?\n)'
    email = open(filename).read()
    try:
        header, body = re.findall(body_pattern, email)[0]
    except IndexError:  # figure out what we want to return here - don't want to add an empty dict to the list
        return {}
    parsed_email = dict(re.findall(header_pattern, header))
    parsed_email['body'] = body
    return parsed_email

emails = []

for dirpath, dirnames, filenames in os.walk('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir'):
    for file in filenames:
        emails.append(parse_email(dirpath, file))


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
        print(k)
        print(email)
        key_errors += 1
    # add rows
    try:
        row = Emails(sent_datetime=dt, **kw)
        session.add(row)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
    finally:
        session.close()

print('Count of KeyErrors: {}'.format(key_errors))
