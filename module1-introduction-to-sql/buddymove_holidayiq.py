# module1-introduction-to-sql/buddymove_holidayiq.py

import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("buddymove_holidayiq.csv")
print(df.dtypes)
print(df.columns)

engine = create_engine('sqlite://')
df.to_sql('review', con=engine)

review = engine.execute("SELECT * FROM review").fetchall()


for row in review:
    print(row[df.columns[0]], row[df.columns[1]],
          row[df.columns[2]], row[df.columns[3]],
          row[df.columns[4]], row[df.columns[5]],
          row[df.columns[6]])


# Count how many rows you have - it should be 249!
# row_count = 249
row_count = """
SELECT count(review."User Id")
FROM review
"""
row_count_result = engine.execute(row_count).fetchall()
print("\nNumber of Rows:", row_count_result[0][0])

# How many users who reviewed at least 100 Nature
# in the category also reviewed at least 100 in
# the Shopping category?

nature_shopping = """
SELECT count(review."User Id")
FROM review
WHERE review."Nature">=100 and review."Shopping">=100
"""

nature_shopping_result = engine.execute(nature_shopping).fetchall()

print("\nNo. of Reviews where Nature >= 100 and Shopping >=100")
print(nature_shopping_result[0][0])


avg_rev = """
SELECT
    avg(review."Sports"),
    avg(review."Religious"),
    avg(review."Nature"),
    avg(review."Theatre"),
    avg(review."Shopping"),
    avg(review."Picnic")
FROM review
"""

avg_rev_results = engine.execute(avg_rev).fetchall()

print('\nAverage Review per Category')
print('---------------------------')
for i in range(0, 5):
    print(f"{df.columns[i + 1]}: {avg_rev_results[0][i]}")