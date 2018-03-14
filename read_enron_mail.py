import os
import os.path
import shutil
import re
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, String, Date, DateTime, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


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


class Addresses(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key = True)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable = False)
    sender = Column(String)
    send_type = Column(String)
    sent_to = Column(String)



#read email and return sender and message ID
def get_metadata(folder, filename):
    filename = os.path.join(folder, filename)
    pattern = r'(?s)(?:([\w-]+)[:]\s*(.*?)\s?\n)'
    email = open(filename).read()
    header = dict(re.findall(pattern, email))
    return header


emails = []

for dirpath, dirnames, filenames in os.walk('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir\\arnold-j'):
    for file in filenames:
        emails.append(get_metadata(dirpath, file))

print(emails[0])

# create session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


for email in emails:
    # add rows
    try:
        row = Emails(message_id=email['Message-ID'], sent_datetime=email['Date'], message_from=email['From'])
        session.add(row)
        session.commit()
    except SQLAlchemyError as e:
        print(e)
    # also need a handler for key error, as not every email has every key - we just want to skip the field if not present in the email
    finally:
        session.close()












#iterate over files in from_folder and copy them all to to_folder, renaming each with message_from and message_id
def copy_emails(from_folder, to_folder):
    for file in os.listdir(from_folder):
        message_from, message_id = get_metadata(from_folder, file)
        shutil.copy2('{}\\{}'.format(from_folder, file), '{}\\{}_{}'.format(to_folder, message_from, message_id))


#create new folder folder_name for each employee (useful for data cleanup)
def create_folders(folder_name):
    for folder in os.listdir('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir'):
        os.chdir('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir\\{}'.format(folder))
        os.mkdir('{}'.format(folder_name))

