# module2-sql-for-analysis/insert_titanic.py

# Read Passenger Data From the CSV File
import os
from dotenv import load_dotenv
import pandas as pd
import psycopg2 as psycho
from psycopg2.extras import execute_values
import json


CSV_FILEPATH = os.path.join(os.path.dirname(__file__),
                            "..", 
                            "module2-sql-for-analysis", 
                            "titanic.csv")

df = pd.read_csv(CSV_FILEPATH)
print(df.dtypes)
print(df.head())


# Connect to PostgreSQL DataBase

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "Invalid DB_NAME value")
DB_USER = os.getenv("DB_USER", "Invalid DB_USER value")
DB_PW = os.getenv("DB_PW", "Invalid DB_PW value")
DB_HOST = os.getenv("DB_HOST", "Invalid DB_HOST value")


connection = psycho.connect(dbname=DB_NAME,
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

# Insert Data Into Passengers Table

