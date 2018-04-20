import pandas
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import re


engine = create_engine('postgresql://mgow:postgres@localhost:5432/enron_emails', echo = True)

emails = pandas.read_sql_query(
    '''select a.sent_to as sent_to, count(*) as count
    from emails e join addresses a
    on e.id=a.email_id
    where sent_to not in ('klay@enron.com', 'kenneth.lay@enron.com', '')
    and send_type = 'To'
    group by a.sent_to
    order by count(*) desc
    limit 10'''
    , engine)

names = emails['sent_to']
for index, name in enumerate(names):
    new_name = re.split(r"[.@]", name, 1)[0].capitalize()
    names[index]=new_name

chart = sns.barplot(x='sent_to', y='count', data=emails)
plt.show()


