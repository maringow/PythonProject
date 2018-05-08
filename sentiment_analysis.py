import nltk
#from nltk.tokenize import word_tokenize
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


#engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)
#
# # create database session
# Session = sessionmaker()
# Session.configure(bind=engine)
# session = Session()
#
# query = session.query(Emails).filter(func.length(Emails.body)>10)
#
# print(query.statement)
#
# for row in query:
#     body = row.body
#     t_body = nltk.word_tokenize(body)
#     pass



#print([x.body for x in query])


paragraph = 'When I first brought my cat home from the humane society she was a mangy, pitiful animal. It cost a lot to adopt her: forty dollars. And then I had to buy litter, a litterbox, food, and dishes for her to eat out of. Two days after she came home with me she got taken to the pound by the animal warden. There''s a leash law for cats in Fort Collins. If they''re not in your yard they have to be on a leash. Anyway, my cat is my best friend. I''m glad I got her. She sleeps under the covers with me when it''s cold. Sometimes she meows a lot in the middle of the night and wakes me up, though.'

nltk.word_tokenize(paragraph)





