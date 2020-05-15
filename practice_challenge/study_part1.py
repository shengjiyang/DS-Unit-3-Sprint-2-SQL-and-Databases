# practice_challenge/study_part1.py


## Starting From Scratch
import os
import sqlite3

DB_FILEPATH = os.path.join(os.path.dirname(__file__),
                                           "..",
                                           "practice_challenge",
                                           "study_part1.sqlite3")


conn = sqlite3.connect(DB_FILEPATH)
cur = conn.cursor()

create_table = """
CREATE TABLE IF NOT EXISTS
STUDENTS (
STUDENT  TEXT NOT NULL,
STUDIED  BOOLEAN,
GRADE    INTEGER NOT NULL,
AGE      INTEGER NOT NULL,
SEX      TEXT NOT NULL
);
"""

cur.execute(create_table)


# insert_data = """
# INSERT INTO STUDENTS
#     (STUDENT, STUDIED, GRADE, AGE, SEX)
# VALUES
#     ('Lion-O', 'True', 85, 24, 'Male'),
#     ('Cheetara', 'True', 95, 22, 'Female'),
#     ('Mumm-Ra', 'False', 65, 153, 'Male'),
#     ('Snarf', 'False', 70, 15, 'Male'),
#     ('Panthro', 'True', 80, 30, 'Male');
# """

# cur.execute(insert_data)

conn.commit()

avg_age = """
SELECT avg(AGE)
FROM STUDENTS;
"""

avg_age_result = cur.execute(avg_age).fetchall()
print("Average Age:", avg_age_result[0][0])


select_female = """
SELECT STUDENT
FROM STUDENTS
WHERE SEX = 'Female'
"""

females = cur.execute(select_female).fetchall()
print("Females:", females[0][0])


alphabetical = """
SELECT *
FROM STUDENTS
ORDER BY STUDENT
"""

alphabetical_results = cur.execute(alphabetical).fetchall()

print('')
for i in range(0, 5):
    print(alphabetical_results[i][0], alphabetical_results[i][1],
          alphabetical_results[i][2], alphabetical_results[i][3],
          alphabetical_results[i][4])