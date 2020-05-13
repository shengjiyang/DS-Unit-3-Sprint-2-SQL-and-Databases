# module2-sql-for-analysis/insert_titanic.py

# Read Passenger Data From the CSV File
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
from psycopg2.extras import execute_values
import numpy as np
import os
from dotenv import load_dotenv
import pandas as pd
import json

# Ensures that psycopg2 and by extension ElephantSQL
# understand the np.int64 values from the Titanic
# DataFrame
register_adapter(np.int64, psycopg2._psycopg.AsIs)

CSV_FILEPATH = os.path.join(os.path.dirname(__file__),
                            "..", 
                            "module2-sql-for-analysis", 
                            "titanic.csv")

df = pd.read_csv(CSV_FILEPATH)
# Ensures that SQL's PRIMARY KEY and DataFrame's Index
# match up
df.index += 1
print(df.head())

# Connect to PostgreSQL DataBase

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "Invalid DB_NAME value")
DB_USER = os.getenv("DB_USER", "Invalid DB_USER value")
DB_PW = os.getenv("DB_PW", "Invalid DB_PW value")
DB_HOST = os.getenv("DB_HOST", "Invalid DB_HOST value")


connection = psycopg2.connect(dbname=DB_NAME,
                            user=DB_USER,
                            password=DB_PW,
                            host=DB_HOST)

# # Create a Table to Store the Passengers
# # Enumerating Sex as a Binary Category
# enumerate_sex = """
# CREATE TYPE SEX
# AS ENUM ('male', 'female')
# """

cur = connection.cursor()
# cur.execute(enumerate_sex)

insert_table = """
CREATE TABLE IF NOT EXISTS titanic(

ID                       SERIAL PRIMARY KEY,
SURVIVED                 INTEGER NOT NULL,
PCLASS                   INTEGER NOT NULL,
NAME                     TEXT NOT NULL,
SEX                      SEX,
AGE                      INTEGER NOT NULL,
SIBLINGS_SPOUSES_ABOARD  INTEGER NOT NULL,
PARENTS_CHILDREN         INTEGER NOT NULL,
FARE                     NUMERIC NOT NULL
);
"""

cur.execute(insert_table)
connection.commit()

# Insert Data Into Passengers Table
records = df.to_records(index="True")
titanic_data = list(records)
print(len(titanic_data))

insert_data = """
INSERT INTO titanic
(ID, SURVIVED, PCLASS, NAME, SEX, AGE,
SIBLINGS_SPOUSES_ABOARD, PARENTS_CHILDREN,
FARE) VALUES%s
"""

execute_values(cur, insert_data, titanic_data)
connection.commit()