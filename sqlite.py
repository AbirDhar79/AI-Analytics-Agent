import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Drop all tables in dependency order so re-runs are safe
for table in ("SALES", "PRODUCT", "EMPLOYEE", "DEPARTMENT", "STUDENT"):
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

# ── STUDENT ───────────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE STUDENT (
    ID      INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME    VARCHAR(50),
    CLASS   VARCHAR(50),
    SECTION VARCHAR(10),
    MARKS   INTEGER,
    AGE     INTEGER
)
""")

students = [
    ("Krish",   "Data Science",     "A", 90, 21),
    ("John",    "Data Science",     "B", 100, 22),
    ("Mukesh",  "Data Science",     "A", 86, 20),
    ("Jacob",   "DevOps",           "A", 50, 23),
    ("Dipesh",  "DevOps",           "A", 35, 22),
    ("Aisha",   "Machine Learning", "B", 92, 21),
    ("Riya",    "Machine Learning", "A", 78, 20),
    ("Tom",     "Data Science",     "C", 65, 24),
    ("Sara",    "DevOps",           "B", 72, 22),
    ("Liam",    "Machine Learning", "C", 88, 21),
    ("Nina",    "Data Science",     "A", 95, 20),
    ("Omar",    "DevOps",           "B", 45, 23),
    ("Priya",   "Machine Learning", "A", 81, 22),
    ("Alex",    "Data Science",     "B", 70, 21),
    ("Mia",     "DevOps",           "C", 55, 24),
    ("Ben",     "Machine Learning", "B", 63, 20),
    ("Zara",    "Data Science",     "A", 99, 21),
    ("Eli",     "DevOps",           "A", 77, 22),
    ("Nora",    "Machine Learning", "C", 84, 23),
    ("Leo",     "Data Science",     "B", 58, 20),
    ("Eva",     "DevOps",           "A", 91, 22),
    ("Dan",     "Machine Learning", "B", 74, 21),
    ("Ivy",     "Data Science",     "C", 82, 20),
    ("Kai",     "DevOps",           "A", 67, 23),
    ("Ava",     "Machine Learning", "A", 96, 21),
]
cursor.executemany(
    "INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS, AGE) VALUES (?, ?, ?, ?, ?)",
    students,
)

# ── DEPARTMENT ────────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE DEPARTMENT (
    ID         INTEGER PRIMARY KEY,
    NAME       VARCHAR(50),
    BUDGET     REAL,
    HEAD_COUNT INTEGER
)
""")

departments = [
    (1, "Engineering", 500000.00, 30),
    (2, "Sales",       300000.00, 20),
    (3, "Marketing",   200000.00, 15),
    (4, "HR",          150000.00, 10),
    (5, "Finance",     250000.00, 12),
]
cursor.executemany("INSERT INTO DEPARTMENT VALUES (?, ?, ?, ?)", departments)

# ── EMPLOYEE ──────────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE EMPLOYEE (
    ID            INTEGER PRIMARY KEY,
    NAME          VARCHAR(50),
    DEPARTMENT_ID INTEGER,
    SALARY        REAL,
    HIRE_DATE     DATE,
    CITY          VARCHAR(50),
    FOREIGN KEY (DEPARTMENT_ID) REFERENCES DEPARTMENT(ID)
)
""")

employees = [
    (1,  "Alice Johnson",  1, 95000,  "2019-03-15", "New York"),
    (2,  "Bob Smith",      2, 72000,  "2020-07-01", "Chicago"),
    (3,  "Carol White",    1, 105000, "2018-11-20", "San Francisco"),
    (4,  "David Brown",    3, 68000,  "2021-02-10", "Los Angeles"),
    (5,  "Emma Davis",     4, 62000,  "2022-05-18", "New York"),
    (6,  "Frank Miller",   2, 78000,  "2019-09-05", "Chicago"),
    (7,  "Grace Wilson",   1, 112000, "2017-04-22", "Seattle"),
    (8,  "Henry Moore",    5, 88000,  "2020-12-01", "Boston"),
    (9,  "Iris Taylor",    3, 71000,  "2021-08-14", "Los Angeles"),
    (10, "Jack Anderson",  2, 65000,  "2023-01-09", "Chicago"),
    (11, "Kara Thomas",    1, 98000,  "2018-06-30", "New York"),
    (12, "Liam Jackson",   4, 55000,  "2022-11-25", "Houston"),
    (13, "Maya Harris",    5, 92000,  "2019-10-17", "Boston"),
    (14, "Noah Martin",    3, 74000,  "2020-04-03", "Los Angeles"),
    (15, "Olivia Garcia",  2, 81000,  "2021-06-19", "Miami"),
    (16, "Paul Martinez",  1, 107000, "2017-12-08", "Seattle"),
    (17, "Quinn Robinson", 4, 59000,  "2023-03-22", "Houston"),
    (18, "Rachel Clark",   5, 96000,  "2018-08-11", "Boston"),
    (19, "Sam Lewis",      2, 69000,  "2022-02-28", "Chicago"),
    (20, "Tina Lee",       3, 77000,  "2020-09-16", "New York"),
    (21, "Uma Perez",      1, 115000, "2016-11-04", "San Francisco"),
    (22, "Victor Hall",    5, 83000,  "2019-07-23", "Boston"),
    (23, "Wendy Young",    2, 76000,  "2021-04-07", "Miami"),
    (24, "Xander King",    3, 72000,  "2020-01-15", "Los Angeles"),
    (25, "Yara Scott",     4, 58000,  "2023-06-11", "New York"),
]
cursor.executemany("INSERT INTO EMPLOYEE VALUES (?, ?, ?, ?, ?, ?)", employees)

# ── PRODUCT ───────────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE PRODUCT (
    ID        INTEGER PRIMARY KEY,
    NAME      VARCHAR(100),
    CATEGORY  VARCHAR(50),
    PRICE     REAL,
    STOCK_QTY INTEGER
)
""")

products = [
    (1,  "Laptop Pro 15",              "Electronics",   1299.99, 45),
    (2,  "Wireless Mouse",             "Electronics",     29.99, 200),
    (3,  "Standing Desk",              "Furniture",       549.00, 30),
    (4,  "Noise Cancelling Headphones","Electronics",    249.99, 80),
    (5,  "Office Chair",               "Furniture",       389.00, 25),
    (6,  "USB-C Hub",                  "Electronics",     49.99, 150),
    (7,  "Monitor 27 inch",            "Electronics",    399.99, 60),
    (8,  "Webcam HD",                  "Electronics",     89.99, 120),
    (9,  "Mechanical Keyboard",        "Electronics",    139.99, 90),
    (10, "Desk Lamp",                  "Office Supplies",  45.00, 175),
    (11, "Notebook Set",               "Office Supplies",  12.99, 300),
    (12, "Whiteboard",                 "Office Supplies",  79.99, 40),
    (13, "Ergonomic Mousepad",         "Office Supplies",  19.99, 250),
    (14, "Tablet 10 inch",             "Electronics",    499.99, 55),
    (15, "Bookshelf",                  "Furniture",       229.00, 20),
    (16, "Cable Management Kit",       "Office Supplies",  24.99, 180),
    (17, "Smart Speaker",              "Electronics",     99.99, 70),
    (18, "Filing Cabinet",             "Furniture",       179.00, 18),
    (19, "Printer All-in-One",         "Electronics",    299.99, 35),
    (20, "Coffee Maker",               "Appliances",      59.99, 50),
    (21, "Mini Fridge",                "Appliances",     149.99, 22),
    (22, "Projector",                  "Electronics",    649.99, 15),
    (23, "Phone Stand",                "Accessories",     14.99, 320),
    (24, "Power Strip",                "Accessories",     34.99, 140),
    (25, "Backpack Laptop Bag",        "Accessories",     69.99, 95),
]
cursor.executemany("INSERT INTO PRODUCT VALUES (?, ?, ?, ?, ?)", products)

# ── SALES ─────────────────────────────────────────────────────────────────────
cursor.execute("""
CREATE TABLE SALES (
    ID           INTEGER PRIMARY KEY,
    PRODUCT_ID   INTEGER,
    EMPLOYEE_ID  INTEGER,
    QUANTITY     INTEGER,
    SALE_DATE    DATE,
    TOTAL_AMOUNT REAL,
    FOREIGN KEY (PRODUCT_ID)  REFERENCES PRODUCT(ID),
    FOREIGN KEY (EMPLOYEE_ID) REFERENCES EMPLOYEE(ID)
)
""")

sales = [
    (1,  1,  2,  2,  "2024-01-05", 2599.98),
    (2,  4,  6,  5,  "2024-01-10", 1249.95),
    (3,  7,  15, 3,  "2024-01-15", 1199.97),
    (4,  2,  10, 10, "2024-01-18",  299.90),
    (5,  9,  2,  4,  "2024-01-22",  559.96),
    (6,  14, 19, 2,  "2024-02-03",  999.98),
    (7,  3,  23, 1,  "2024-02-07",  549.00),
    (8,  5,  6,  2,  "2024-02-14",  778.00),
    (9,  17, 15, 6,  "2024-02-18",  599.94),
    (10, 11, 10, 20, "2024-02-25",  259.80),
    (11, 22, 2,  1,  "2024-03-02",  649.99),
    (12, 8,  19, 4,  "2024-03-08",  359.96),
    (13, 6,  23, 8,  "2024-03-12",  399.92),
    (14, 13, 6,  15, "2024-03-19",  299.85),
    (15, 19, 15, 2,  "2024-03-25",  599.98),
    (16, 1,  10, 1,  "2024-04-01", 1299.99),
    (17, 24, 2,  12, "2024-04-06",  419.88),
    (18, 25, 19, 5,  "2024-04-11",  349.95),
    (19, 20, 23, 3,  "2024-04-17",  179.97),
    (20, 15, 6,  1,  "2024-04-22",  229.00),
    (21, 7,  10, 2,  "2024-05-02",  799.98),
    (22, 4,  15, 3,  "2024-05-09",  749.97),
    (23, 21, 2,  2,  "2024-05-14",  299.98),
    (24, 12, 19, 1,  "2024-05-20",   79.99),
    (25, 10, 23, 8,  "2024-05-27",  360.00),
    (26, 2,  6,  15, "2024-06-03",  449.85),
    (27, 9,  10, 3,  "2024-06-10",  419.97),
    (28, 17, 15, 4,  "2024-06-16",  399.96),
    (29, 14, 2,  1,  "2024-06-21",  499.99),
    (30, 3,  19, 2,  "2024-06-28", 1098.00),
]
cursor.executemany("INSERT INTO SALES VALUES (?, ?, ?, ?, ?, ?)", sales)

# ── Summary ───────────────────────────────────────────────────────────────────
connection.commit()

print("student.db created successfully.")
for table in ("STUDENT", "DEPARTMENT", "EMPLOYEE", "PRODUCT", "SALES"):
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {count} rows")

connection.close()
