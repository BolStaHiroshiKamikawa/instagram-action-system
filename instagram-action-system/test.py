import psycopg2
from psycopg2.extras import DictCursor
import os
import configparser
from dateutil.relativedelta import relativedelta
import datetime

config = configparser.ConfigParser()
config.read('../config.ini')

connection = psycopg2.connect(
    f"dbname={os.environ['PSQL_DBNAME']} host={os.environ['PSQL_HOST']} user={os.environ['PSQL_USER']} password={os.environ['PSQL_PASSWORD']} sslmode={config['POSTGRESQL']['SSLMODE']}"
)

cur = connection.cursor(cursor_factory=DictCursor)

cur.execute(f"select * from main_users;")

list = cur.fetchall()

time = list[0]['running_start']
print(time)

connection.close()

time_l = time + relativedelta(months = 3)

now = datetime.datetime.now().replace(tzinfo=datetime.timezone.utc)
print(now)
if now > time_l :
    print('yes')
else :
    print('no')
