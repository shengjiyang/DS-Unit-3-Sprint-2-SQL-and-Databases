# practice_challenge/study_part2.py

import os
import sqlite3
import pandas as pd
import numpy as np

DB_FILEPATH = os.path.join(os.path.dirname(__file__),
                                           "..",
                                           "data",
                                           "chinook.db")


# Find the average invoice total for each customer,
# return the details for the first 5 ID's

# To answer this question, we need the
# Invoices Table.

conn = sqlite3.connect(DB_FILEPATH)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

avg_invoice_total = """
SELECT avg(Total)
FROM invoices
"""

avg_invoice_total_result = cur.execute(avg_invoice_total).fetchall()
print(f"${round(avg_invoice_total_result[0][0], 2)}")

# $5.65

avg_invoice_5 = """
SELECT *
FROM invoices
LIMIT 5
"""

avg_invoice_5_results = cur.execute(avg_invoice_5).fetchall()

for row in avg_invoice_5_results:
    print(row[0], row[1], row[2], row[3], row[4],
          row[5], row[6], row[7], row[8])


# Return all columns in Customer for the first 5
# customers residing in the United States.

US_5 = """
SELECT *
FROM customers
WHERE Country = "USA"
LIMIT 5
"""

US_5_results = cur.execute(US_5).fetchall()

for row in US_5_results:
    print(row[0], row[1], row[2], row[3], row[4], row[5],
          row[6], row[7], row[8], row[9], row[10],
          row[11], row[12])


# Which employee does not report to anyone?
# For this, we'll need to check the employees table.

no_report = """
SELECT *
FROM employees
WHERE ReportsTo IS NULL
"""

no_report_result = cur.execute(no_report).fetchall()
print(no_report_result[0][2], no_report_result[0][1])

# Andrew Adams


# Find the number of unique composers?
# This information is found in the tracks table.

composers = """
SELECT Composer
FROM tracks
"""

composers_results = cur.execute(composers).fetchall()

# Converting the data to a DataFrame in order to
# manipulate it
pd.set_option("display.max_columns", 10)
pd.set_option("display.max_rows", 1000)

df = pd.DataFrame(composers_results)

# id = []
# for i in range(0, len(df[0])):
#     id.append(i)

# df["id"] = id
# df = df[["id", 0]]

df.dropna(inplace=True)

# id = []
# for i in df.id:
#     id.append(i)


df[0] = df[0].str.replace("&", ",",).str.replace("/", ",",).str.replace("-", ",").str.replace(";", ",")
df[0] = df[0].str.replace("AC,DC", "AC/DC")

split = pd.DataFrame(df[0].str.split(",", 5).to_list(),
                     columns = ["One", "Two", "Three", "Four", "Five", "Six"])



# split["id"] = id
# split = split[["id", "One", "Two", "Three", "Four", "Five", "Six"]]

# Reinserting the data into a new table in order to
# answer our question with SQL

# # Temporarily dropping the table.
# drop_table = """
# DROP TABLE composers;
# """

# cur.execute(drop_table)
# conn.commit()

composers_table ="""
CREATE TABLE IF NOT EXISTS composers(
    
    One   TEXT,
    Two   TEXT,
    Three TEXT,
    Four  TEXT,
    Five  TEXT,
    Six   TEXT
);
"""

cur.execute(composers_table)
conn.commit()


# Reinserting the data will require the df to be in a
# particular format.

composers_data = split.to_records(index=False)
composers_data = list(composers_data)


# insert_composers = """
# INSERT INTO composers
# (One, Two, Three, Four, Five, Six)
# VALUES (?, ?, ?, ?, ?, ?)
# """

# conn.executemany(insert_composers, composers_data)
# conn.commit()


# Now to actually answer our question,
# For the purposes of being explicit,
# I have gone through all of the trouble above
# because I have defined composer as individual
# artist, so bands do not count, unless no individual
# artist is listed.

composer_count = """
SELECT
    count(distinct One) +
    count(distinct Two) +
    count(distinct Three) +
    count(distinct Four) +
    count(distinct Five) + 
    count(distinct Six)
FROM composers
WHERE One <> "Vários"
AND One <> "Traditional"
"""

cc_result = cur.execute(composer_count).fetchall()
print(cc_result[0][0])

breakpoint()