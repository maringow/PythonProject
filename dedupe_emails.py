from emails import Emails
from addresses import Addresses
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


emails = session.query(Emails).order_by(Emails.body, Emails.sent_datetime, Emails.message_to).all()
print(emails)
last_email = None


for email in emails:
    print(email)
    if (last_email and email.duplicate_check==last_email.duplicate_check):
        email.duplicate_id = last_email.id
        session.commit()
    else:
        last_email = email
