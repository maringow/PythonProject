from emails import Emails
from addresses import Addresses
from persons import Persons
from address_to_person import AddressToPerson
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import re
from collections import defaultdict
from pprint import pprint


engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)
connection = engine.connect()

result = connection.execute(
'''select filename, sent_to
from emails join addresses
on emails.id = addresses.email_id
where filename like '%%inbox%%'
and sent_to like '%%@enron.com'
and send_type in ('To', 'Cc')
order by filename, sent_to desc'''
)

names_and_emails = defaultdict(dict)

for row in result:
    person = re.findall(r'([a-z]+[-][a-z]+)', row.filename)
    names_and_emails[person[0]].setdefault(row.sent_to, 0)
    names_and_emails[person[0]][row.sent_to] +=1

connection.close()

# create database session
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

for person, emails in names_and_emails.items():
    name = person.split('-')[0]
    #sorted_emails = sorted(emails.items(), key=lambda pair:pair[-1])
    sorted_emails = sorted([(count, address) for address, count in emails.items()], reverse=1)
    #sorted emails up to 5
    for count, address in sorted_emails[:5]:
        if name in address:
            print(address)
            row = AddressToPerson(address=address, person=person)
            #insert person, address into address_to_person table
            session.add(row)
            session.commit()





