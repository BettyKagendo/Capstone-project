import psycopg2
from decouple import config

#establish a connection
try:
    conn = psycopg2.connect(
       dbname=config('database'),
       user='postgres',
       password=config('password'),
       host='localhost'
    )
    print ('Connected to the  database')
except psycopg2.Error as err:
    print ("Unable to connect to the database: ", err)                                                         