import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "hr.db"
connection = sqlite3.connect(str(db_path))
cursor = connection.cursor()

for table in ("LEAVE_REQUEST", "PERFORMANCE", "JOB_POSTING", "EMPLOYEE", "DEPARTMENT"):
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

cursor.execute("""
CREATE TABLE DEPARTMENT (
    ID         INTEGER PRIMARY KEY,
    NAME       VARCHAR(50),
    LOCATION   VARCHAR(50),
    BUDGET     REAL,
    HEAD_COUNT INTEGER
)
""")

departments = [
    (1, "Engineering", "San Francisco", 1200000.00, 18),
    (2, "Sales",       "New York",       600000.00, 12),
    (3, "Marketing",   "Chicago",        400000.00,  9),
    (4, "HR",          "Austin",         250000.00,  6),
    (5, "Finance",     "Boston",         500000.00,  8),
]
cursor.executemany("INSERT INTO DEPARTMENT VALUES (?,?,?,?,?)", departments)

cursor.execute("""
CREATE TABLE EMPLOYEE (
    ID            INTEGER PRIMARY KEY,
    NAME          VARCHAR(100),
    DEPARTMENT_ID INTEGER,
    JOB_TITLE     VARCHAR(100),
    SALARY        REAL,
    HIRE_DATE     DATE,
    MANAGER_ID    INTEGER,
    STATUS        VARCHAR(20),
    FOREIGN KEY (DEPARTMENT_ID) REFERENCES DEPARTMENT(ID),
    FOREIGN KEY (MANAGER_ID)    REFERENCES EMPLOYEE(ID)
)
""")

employees = [
    (1,  "Diana Prince",    1, "VP of Engineering",   145000, "2016-03-14", None, "Active"),
    (2,  "Clark Kent",      2, "VP of Sales",         135000, "2017-07-22", None, "Active"),
    (3,  "Bruce Banner",    3, "VP of Marketing",     128000, "2017-11-05", None, "Active"),
    (4,  "Natasha Romanov", 4, "HR Director",         118000, "2018-02-19", None, "Active"),
    (5,  "Tony Stark",      5, "CFO",                 160000, "2015-09-01", None, "Active"),
    (6,  "Peter Parker",    1, "Senior Engineer",      98000, "2019-05-20",  1,   "Active"),
    (7,  "Wanda Maximoff",  1, "Software Engineer",    82000, "2021-08-10",  6,   "Active"),
    (8,  "Steve Rogers",    1, "Lead Engineer",       112000, "2018-04-15",  1,   "Active"),
    (9,  "Thor Odinson",    2, "Senior Sales Rep",     88000, "2020-01-09",  2,   "Active"),
    (10, "Loki Laufeyson",  2, "Sales Rep",            72000, "2022-03-17",  9,   "On Leave"),
    (11, "Carol Danvers",   2, "Account Manager",      95000, "2019-10-28",  2,   "Active"),
    (12, "Scott Lang",      3, "Marketing Manager",    90000, "2020-06-04",  3,   "Active"),
    (13, "Hope Van Dyne",   3, "Content Strategist",   78000, "2021-11-22", 12,   "Active"),
    (14, "Sam Wilson",      3, "SEO Specialist",       74000, "2022-07-30", 12,   "Active"),
    (15, "Bucky Barnes",    4, "HR Manager",           85000, "2019-03-12",  4,   "Active"),
    (16, "Maria Hill",      4, "Recruiter",            68000, "2022-09-05", 15,   "Active"),
    (17, "Nick Fury",       5, "Senior Accountant",    96000, "2018-12-01",  5,   "Active"),
    (18, "Pepper Potts",    5, "Financial Analyst",    88000, "2020-02-14",  5,   "Active"),
    (19, "James Rhodes",    1, "DevOps Engineer",      92000, "2021-04-27",  8,   "Active"),
    (20, "Vision",          1, "Data Scientist",      105000, "2020-08-16",  1,   "Terminated"),
    (21, "Gamora",          2, "Business Dev Rep",     76000, "2023-01-09",  2,   "Active"),
    (22, "Rocket",          3, "Digital Ad Manager",   80000, "2022-05-18", 12,   "Active"),
    (23, "Groot",           4, "HR Coordinator",       62000, "2023-03-22", 15,   "Active"),
    (24, "Drax",            5, "Payroll Specialist",   70000, "2021-10-11",  5,   "Active"),
    (25, "Star Lord",       1, "QA Engineer",          86000, "2022-11-07",  6,   "On Leave"),
]
cursor.executemany("INSERT INTO EMPLOYEE VALUES (?,?,?,?,?,?,?,?)", employees)

cursor.execute("""
CREATE TABLE PERFORMANCE (
    ID            INTEGER PRIMARY KEY,
    EMPLOYEE_ID   INTEGER,
    REVIEW_YEAR   INTEGER,
    RATING        INTEGER,
    BONUS_AMOUNT  REAL,
    FOREIGN KEY (EMPLOYEE_ID) REFERENCES EMPLOYEE(ID)
)
""")

performance = [
    (1,  6,  2022, 5, 12000),
    (2,  6,  2023, 4,  9000),
    (3,  7,  2022, 3,  4500),
    (4,  7,  2023, 4,  7000),
    (5,  8,  2022, 5, 14000),
    (6,  8,  2023, 5, 15000),
    (7,  9,  2022, 4,  8000),
    (8,  9,  2023, 3,  5000),
    (9,  10, 2022, 2,  2000),
    (10, 11, 2022, 4,  9500),
    (11, 11, 2023, 5, 13000),
    (12, 12, 2022, 4,  8500),
    (13, 12, 2023, 4,  9000),
    (14, 13, 2023, 3,  4000),
    (15, 14, 2023, 4,  6000),
    (16, 15, 2022, 5, 11000),
    (17, 15, 2023, 4,  9500),
    (18, 17, 2022, 4,  9000),
    (19, 17, 2023, 5, 12000),
    (20, 18, 2022, 3,  5000),
    (21, 18, 2023, 4,  7500),
    (22, 19, 2023, 4,  8000),
    (23, 21, 2023, 3,  4500),
    (24, 22, 2023, 4,  7000),
    (25, 24, 2023, 3,  5500),
]
cursor.executemany("INSERT INTO PERFORMANCE VALUES (?,?,?,?,?)", performance)

cursor.execute("""
CREATE TABLE LEAVE_REQUEST (
    ID          INTEGER PRIMARY KEY,
    EMPLOYEE_ID INTEGER,
    LEAVE_TYPE  VARCHAR(20),
    START_DATE  DATE,
    END_DATE    DATE,
    DAYS        INTEGER,
    STATUS      VARCHAR(20),
    FOREIGN KEY (EMPLOYEE_ID) REFERENCES EMPLOYEE(ID)
)
""")

leave_requests = [
    (1,  7,  "Annual",  "2024-01-08", "2024-01-12",  5, "Approved"),
    (2,  10, "Sick",    "2024-01-15", "2024-01-17",  3, "Approved"),
    (3,  13, "Annual",  "2024-02-05", "2024-02-09",  5, "Approved"),
    (4,  16, "Annual",  "2024-02-19", "2024-02-23",  5, "Approved"),
    (5,  9,  "Sick",    "2024-03-04", "2024-03-05",  2, "Approved"),
    (6,  19, "Annual",  "2024-03-11", "2024-03-15",  5, "Approved"),
    (7,  21, "Unpaid",  "2024-03-25", "2024-03-29",  5, "Rejected"),
    (8,  14, "Annual",  "2024-04-08", "2024-04-12",  5, "Approved"),
    (9,  25, "Sick",    "2024-04-15", "2024-04-18",  4, "Approved"),
    (10, 22, "Annual",  "2024-04-22", "2024-04-26",  5, "Approved"),
    (11, 6,  "Annual",  "2024-05-06", "2024-05-10",  5, "Approved"),
    (12, 18, "Sick",    "2024-05-13", "2024-05-14",  2, "Approved"),
    (13, 24, "Annual",  "2024-05-20", "2024-05-24",  5, "Approved"),
    (14, 11, "Annual",  "2024-06-03", "2024-06-07",  5, "Approved"),
    (15, 23, "Unpaid",  "2024-06-10", "2024-06-14",  5, "Pending"),
    (16, 8,  "Annual",  "2024-06-17", "2024-06-21",  5, "Approved"),
    (17, 15, "Sick",    "2024-07-01", "2024-07-03",  3, "Approved"),
    (18, 19, "Annual",  "2024-07-08", "2024-07-19", 10, "Pending"),
    (19, 7,  "Sick",    "2024-07-22", "2024-07-22",  1, "Approved"),
    (20, 21, "Annual",  "2024-08-05", "2024-08-09",  5, "Pending"),
]
cursor.executemany("INSERT INTO LEAVE_REQUEST VALUES (?,?,?,?,?,?,?)", leave_requests)

cursor.execute("""
CREATE TABLE JOB_POSTING (
    ID                   INTEGER PRIMARY KEY,
    TITLE                VARCHAR(100),
    DEPARTMENT_ID        INTEGER,
    POSTED_DATE          DATE,
    CLOSE_DATE           DATE,
    STATUS               VARCHAR(20),
    APPLICATIONS_RECEIVED INTEGER,
    FOREIGN KEY (DEPARTMENT_ID) REFERENCES DEPARTMENT(ID)
)
""")

job_postings = [
    (1,  "Backend Engineer",        1, "2024-01-10", "2024-02-10", "Filled",  48),
    (2,  "Frontend Engineer",       1, "2024-01-15", "2024-02-15", "Filled",  36),
    (3,  "Sales Representative",    2, "2024-02-01", "2024-03-01", "Filled",  62),
    (4,  "Account Executive",       2, "2024-02-20", "2024-03-20", "Open",    29),
    (5,  "Content Writer",          3, "2024-03-05", "2024-04-05", "Filled",  41),
    (6,  "Performance Marketer",    3, "2024-03-15", "2024-04-15", "Open",    22),
    (7,  "HR Generalist",           4, "2024-04-01", "2024-05-01", "Closed",  18),
    (8,  "Data Scientist",          1, "2024-04-10", "2024-05-10", "Open",    55),
    (9,  "Financial Controller",    5, "2024-05-01", "2024-06-01", "Open",    17),
    (10, "DevOps Engineer",         1, "2024-05-20", "2024-06-20", "Open",    33),
]
cursor.executemany("INSERT INTO JOB_POSTING VALUES (?,?,?,?,?,?,?)", job_postings)

connection.commit()
print("hr.db created successfully.")
for table in ("DEPARTMENT", "EMPLOYEE", "PERFORMANCE", "LEAVE_REQUEST", "JOB_POSTING"):
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {count} rows")
connection.close()
