import os
import os.path
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dateutil import parser
from addresses import Addresses
from emails import Emails


engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)


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
    parsed_email['filename'] = filename
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
    # try:
    #     kw = {Emails.key_by_label[label]:value for label, value in email.items()}
    #     dt = parser.parse(kw.pop('sent_datetime'))
    #     fn = email['filename']
    #     # print(kw)
    # except KeyError as k:
    #     print('KeyError in message {}: {}'.format(email, k))
    #     key_errors += 1
    # # add rows
    # except ValueError as v:
    #     print('ValueError in message {}: {}'.format(email, v))
    try:
        kw = {Emails.key_by_label[label]:value for label, value in email.items()}
        dt = parser.parse(kw.pop('sent_datetime'))
        fn = email['filename']
        emails_row = Emails(sent_datetime=dt, filename=fn, **kw)
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
    except KeyError as k:
        print('KeyError in message {}: {}'.format(email, k))
        key_errors += 1
    # add rows
    except ValueError as v:
        print('ValueError in message {}: {}'.format(email, v))
    except SQLAlchemyError as e:
        print(e)
    finally:
        session.close()

print('Count of KeyErrors: {}'.format(key_errors))
