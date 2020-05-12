# inclass/elephant.py

import os
import psycopg2 as psycho
DB_NAME = os.getenv("DB_NAME", "Invalid DB_NAME value")
DB_USER = os.getenv("DB_USER", "Invalid DB_USER value")
DB_PW = os.getenv("DB_PW", "Invalid DB_PW value")
DB_HOST = os.getenv("DB_HOST", "Invalid DB_HOST value")
connection = psycho.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PW,
                            host=DB_HOST)


exit()

print(type(connection)) #> <class 'psycopg2.extensions.connection'>
cursor = connection.cursor()
print(type(cursor)) #> <class 'psycopg2.extensions.cursor'>
cursor.execute("SELECT * from test_table;")
#results = cursor.fetchone()
results = cursor.fetchall()
for row in results:
    print(type(row), row)
