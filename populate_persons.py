import os
import os.path
import re
from persons import Persons
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


#engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)

# create database session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


for directory in os.listdir('C:\\Users\\MGOW\\Documents\\PythonProject\\maildir'):
    name_row = Persons(name = directory)
    session.add(name_row)
    session.commit()