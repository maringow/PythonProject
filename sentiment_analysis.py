from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from addresses import Addresses
from emails import Emails
from sqlalchemy.sql.expression import func


engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)

# create database session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

query = session.query(Emails).filter(func.length(Emails.body)>10)

print(query.statement)

for row in query:
    body = row.body
    t_body = word_tokenize(body)
    pass



#print([x.body for x in query])







