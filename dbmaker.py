from faker import Faker
import pprint
import sqlite3
import random

fake = Faker('uk_UA')
conn = sqlite3.connect('university.db')
cur = conn.cursor()

# Створюємо таблиці
cur.execute('''CREATE TABLE Groups (
                id INTEGER PRIMARY KEY,
                name TEXT
                );''')

cur.execute('''CREATE TABLE Teachers (
                id INTEGER PRIMARY KEY,
                name TEXT
                );''')

cur.execute('''CREATE TABLE Subjects (
                id INTEGER PRIMARY KEY,
                name TEXT,
                teacher_id INTEGER,
                FOREIGN KEY (teacher_id) REFERENCES Teachers(id)
                );''')

cur.execute('''CREATE TABLE Students (
                id INTEGER PRIMARY KEY,
                name TEXT,
                group_id INTEGER,
                FOREIGN KEY (group_id) REFERENCES Groups(id)
                );''')

cur.execute('''CREATE TABLE Grades (
                id INTEGER PRIMARY KEY,
                student_id INTEGER,
                subject_id INTEGER,
                grade INTEGER,
                date_received TEXT,
                FOREIGN KEY (student_id) REFERENCES Students(id),
                FOREIGN KEY (subject_id) REFERENCES Subjects(id)
                );''')

# Students
for _ in range(50):
    full_name = fake.name()
    group_id = random.randint(1, 3)
    cur.execute("INSERT INTO Students (name, group_id) VALUES (?, ?)",
                (full_name, group_id))
conn.commit()

# Groups
groups = ['Group 1', 'Group 2', 'Group 3', 'Group 4', 'Group 5']

for group_name in groups:
    cur.execute("INSERT INTO Groups (name) VALUES (?)", (group_name,))
conn.commit()

# Professors
for _ in range(5):
    professor_name = fake.name()
    cur.execute("INSERT INTO Teachers (name) VALUES (?)", (professor_name,))
conn.commit()

# Subjects
subjects = ['Astronomy', 'Physics', 'Art', 'Data engineering', 'Geology']
for subject_name in subjects:
    teacher_id = random.randint(1, 5)
    cur.execute("INSERT INTO Subjects (name, teacher_id) VALUES (?, ?)",
                (subject_name, teacher_id))
conn.commit()

# Grades
for student_id in range(1, 51):
    for subject_id in range(1, 6):
        for _ in range(random.randint(1, 5)):
            grade = round(random.uniform(60, 100), 2)
            date_received = fake.date_between(start_date='-1y', end_date='today')
            cur.execute("INSERT INTO Grades (student_id, subject_id, grade, date_received) VALUES (?, ?, ?, ?)",
                        (student_id, subject_id, grade, date_received))
conn.commit()


def execute_query(cursor, query_number):
    file_path = f"DB/query{query_number}.sql"
    with open(file_path, 'r', encoding='utf-8') as file:
        query = file.read()
        print(query.split('/n')[0])
        cursor.execute(query)


execute_query(cur, 10)
result = cur.fetchall()
for row in result:
    pprint.pprint(row)

cur.close()
conn.close()
