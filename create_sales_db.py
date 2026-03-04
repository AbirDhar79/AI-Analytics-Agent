import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / "sales.db"
connection = sqlite3.connect(str(db_path))
cursor = connection.cursor()

for table in ("ORDER_ITEM", "ORDERS", "CAMPAIGN", "PRODUCT", "CUSTOMER"):
    cursor.execute(f"DROP TABLE IF EXISTS {table}")

cursor.execute("""
CREATE TABLE CUSTOMER (
    ID          INTEGER PRIMARY KEY,
    NAME        VARCHAR(100),
    EMAIL       VARCHAR(100),
    CITY        VARCHAR(50),
    SIGNUP_DATE DATE,
    SEGMENT     VARCHAR(20)
)
""")

customers = [
    (1,  "Alice Monroe",   "alice@email.com",   "New York",     "2022-01-15", "Retail"),
    (2,  "Bob Carter",     "bob@email.com",     "Chicago",      "2021-06-20", "Wholesale"),
    (3,  "Carol Singh",    "carol@email.com",   "Los Angeles",  "2023-03-10", "Online"),
    (4,  "David Kim",      "david@email.com",   "Houston",      "2022-09-05", "Retail"),
    (5,  "Emma Patel",     "emma@email.com",    "Phoenix",      "2021-11-22", "Online"),
    (6,  "Frank Lopez",    "frank@email.com",   "Philadelphia", "2023-01-08", "Wholesale"),
    (7,  "Grace Lee",      "grace@email.com",   "San Antonio",  "2022-04-17", "Retail"),
    (8,  "Henry Nguyen",   "henry@email.com",   "San Diego",    "2021-07-30", "Online"),
    (9,  "Iris Johnson",   "iris@email.com",    "Dallas",       "2023-05-14", "Retail"),
    (10, "Jack Williams",  "jack@email.com",    "San Jose",     "2022-08-25", "Wholesale"),
    (11, "Karen Davis",    "karen@email.com",   "Austin",       "2021-03-12", "Online"),
    (12, "Leo Martinez",   "leo@email.com",     "Jacksonville", "2023-07-19", "Retail"),
    (13, "Maya Thompson",  "maya@email.com",    "Fort Worth",   "2022-02-28", "Wholesale"),
    (14, "Nathan Brown",   "nathan@email.com",  "Columbus",     "2021-10-04", "Retail"),
    (15, "Olivia Garcia",  "olivia@email.com",  "Charlotte",    "2023-09-22", "Online"),
    (16, "Paul Wilson",    "paul@email.com",    "Indianapolis", "2022-06-11", "Retail"),
    (17, "Quinn Moore",    "quinn@email.com",   "Seattle",      "2021-12-01", "Wholesale"),
    (18, "Rachel Taylor",  "rachel@email.com",  "Denver",       "2023-02-16", "Online"),
    (19, "Sam Anderson",   "sam@email.com",     "Washington",   "2022-11-07", "Retail"),
    (20, "Tina Thomas",    "tina@email.com",    "Nashville",    "2021-05-23", "Wholesale"),
    (21, "Uma Jackson",    "uma@email.com",     "Baltimore",    "2023-04-30", "Online"),
    (22, "Victor White",   "victor@email.com",  "Louisville",   "2022-07-14", "Retail"),
    (23, "Wendy Harris",   "wendy@email.com",   "Portland",     "2021-09-08", "Wholesale"),
    (24, "Xander Lewis",   "xander@email.com",  "Las Vegas",    "2023-06-25", "Online"),
    (25, "Yara Robinson",  "yara@email.com",    "Memphis",      "2022-03-19", "Retail"),
]
cursor.executemany("INSERT INTO CUSTOMER VALUES (?,?,?,?,?,?)", customers)

cursor.execute("""
CREATE TABLE PRODUCT (
    ID          INTEGER PRIMARY KEY,
    NAME        VARCHAR(100),
    CATEGORY    VARCHAR(50),
    PRICE       REAL,
    COST_PRICE  REAL,
    STOCK_QTY   INTEGER
)
""")

products = [
    (1,  "Running Shoes",          "Footwear",       89.99,  42.00, 120),
    (2,  "Casual T-Shirt",         "Clothing",       24.99,  10.00, 300),
    (3,  "Bluetooth Speaker",      "Electronics",   129.99,  65.00,  80),
    (4,  "Coffee Maker",           "Appliances",     59.99,  28.00,  60),
    (5,  "Yoga Mat",               "Sports",         35.00,  14.00, 150),
    (6,  "Desk Lamp",              "Home & Office",  45.00,  18.00, 200),
    (7,  "Protein Powder 2kg",     "Nutrition",      54.99,  22.00,  90),
    (8,  "Wireless Earbuds",       "Electronics",   119.99,  55.00, 110),
    (9,  "Jeans Slim Fit",         "Clothing",       49.99,  20.00, 180),
    (10, "Stainless Water Bottle", "Sports",         22.99,   8.00, 250),
    (11, "Laptop Backpack",        "Bags",           69.99,  30.00,  95),
    (12, "Sunglasses UV400",       "Accessories",    39.99,  15.00, 140),
    (13, "Bestseller Novel",       "Books",          15.99,   5.00, 400),
    (14, "Indoor Plant Pot",       "Home & Office",  29.99,  11.00, 160),
    (15, "Electric Toothbrush",    "Health",         49.99,  22.00,  70),
    (16, "Gaming Mouse",           "Electronics",    79.99,  38.00, 100),
    (17, "Hoodie Zip-Up",          "Clothing",       59.99,  25.00, 130),
    (18, "Cast Iron Pan",          "Kitchen",        44.99,  19.00,  55),
    (19, "Resistance Bands Set",   "Sports",         19.99,   7.00, 220),
    (20, "Scented Candle Set",     "Home & Office",  27.99,  10.00, 175),
    (21, "Smart Watch",            "Electronics",   199.99,  95.00,  45),
    (22, "Vitamin D3 Supplement",  "Health",         14.99,   5.00, 310),
    (23, "Leather Wallet",         "Accessories",    34.99,  13.00, 115),
    (24, "Portable Charger",       "Electronics",    39.99,  17.00, 135),
    (25, "Foam Roller",            "Sports",         25.99,   9.00, 190),
]
cursor.executemany("INSERT INTO PRODUCT VALUES (?,?,?,?,?,?)", products)

cursor.execute("""
CREATE TABLE ORDERS (
    ID           INTEGER PRIMARY KEY,
    CUSTOMER_ID  INTEGER,
    ORDER_DATE   DATE,
    STATUS       VARCHAR(20),
    TOTAL_AMOUNT REAL,
    FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER(ID)
)
""")

orders = [
    (1,  3,  "2024-01-05", "Delivered",  152.98),
    (2,  7,  "2024-01-10", "Delivered",   89.99),
    (3,  12, "2024-01-18", "Shipped",    204.97),
    (4,  1,  "2024-01-25", "Delivered",   74.98),
    (5,  20, "2024-02-02", "Cancelled",   49.99),
    (6,  5,  "2024-02-08", "Delivered",  229.97),
    (7,  9,  "2024-02-14", "Delivered",   64.99),
    (8,  15, "2024-02-19", "Shipped",    139.98),
    (9,  22, "2024-02-25", "Delivered",   89.99),
    (10, 4,  "2024-03-03", "Delivered",  104.98),
    (11, 18, "2024-03-09", "Pending",     79.99),
    (12, 11, "2024-03-15", "Delivered",  199.99),
    (13, 25, "2024-03-21", "Delivered",   64.97),
    (14, 6,  "2024-03-28", "Shipped",    109.98),
    (15, 2,  "2024-04-04", "Delivered",  152.98),
    (16, 14, "2024-04-10", "Cancelled",   35.00),
    (17, 19, "2024-04-16", "Delivered",  119.99),
    (18, 8,  "2024-04-22", "Delivered",   57.98),
    (19, 23, "2024-04-28", "Shipped",    189.98),
    (20, 10, "2024-05-05", "Delivered",   84.98),
    (21, 17, "2024-05-11", "Delivered",  129.98),
    (22, 13, "2024-05-17", "Pending",     54.99),
    (23, 24, "2024-05-23", "Delivered",  149.97),
    (24, 16, "2024-05-29", "Delivered",   89.98),
    (25, 21, "2024-06-04", "Shipped",    219.98),
    (26, 3,  "2024-06-10", "Delivered",   79.99),
    (27, 7,  "2024-06-16", "Delivered",  104.98),
    (28, 12, "2024-06-22", "Pending",     44.99),
    (29, 1,  "2024-06-28", "Delivered",  174.98),
    (30, 5,  "2024-07-04", "Shipped",    249.98),
]
cursor.executemany("INSERT INTO ORDERS VALUES (?,?,?,?,?)", orders)

cursor.execute("""
CREATE TABLE ORDER_ITEM (
    ID          INTEGER PRIMARY KEY,
    ORDER_ID    INTEGER,
    PRODUCT_ID  INTEGER,
    QUANTITY    INTEGER,
    UNIT_PRICE  REAL,
    FOREIGN KEY (ORDER_ID)   REFERENCES ORDERS(ID),
    FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT(ID)
)
""")

order_items = [
    (1,  1,  3,  1, 129.99),
    (2,  1,  10, 1,  22.99),
    (3,  2,  1,  1,  89.99),
    (4,  3,  8,  1, 119.99),
    (5,  3,  17, 1,  59.99),
    (6,  3,  2,  1,  24.99),
    (7,  4,  4,  1,  59.99),
    (8,  4,  12, 1,  39.99),
    (9,  5,  9,  1,  49.99),
    (10, 6,  21, 1, 199.99),
    (11, 6,  22, 2,  14.99),
    (12, 7,  6,  1,  45.00),
    (13, 7,  19, 1,  19.99),
    (14, 8,  16, 1,  79.99),
    (15, 8,  24, 1,  39.99),
    (16, 9,  1,  1,  89.99),
    (17, 10, 5,  2,  35.00),
    (18, 10, 7,  1,  54.99),
    (19, 11, 16, 1,  79.99),
    (20, 12, 21, 1, 199.99),
    (21, 13, 2,  2,  24.99),
    (22, 13, 19, 1,  19.99),
    (23, 14, 8,  1, 119.99),
    (24, 15, 3,  1, 129.99),
    (25, 15, 10, 1,  22.99),
    (26, 16, 5,  1,  35.00),
    (27, 17, 8,  1, 119.99),
    (28, 18, 14, 1,  29.99),
    (29, 18, 20, 1,  27.99),
    (30, 19, 21, 1, 199.99),
    (31, 20, 11, 1,  69.99),
    (32, 20, 23, 1,  34.99),
    (33, 21, 3,  1, 129.99),
    (34, 22, 7,  1,  54.99),
    (35, 23, 17, 1,  59.99),
    (36, 23, 9,  1,  49.99),
    (37, 23, 24, 1,  39.99),
    (38, 24, 1,  1,  89.99),
    (39, 25, 21, 1, 199.99),
    (40, 25, 6,  1,  45.00),
    (41, 26, 16, 1,  79.99),
    (42, 27, 4,  1,  59.99),
    (43, 27, 12, 1,  39.99),
    (44, 28, 18, 1,  44.99),
    (45, 29, 21, 1, 199.99),
    (46, 30, 8,  1, 119.99),
    (47, 30, 3,  1, 129.99),
]
cursor.executemany("INSERT INTO ORDER_ITEM VALUES (?,?,?,?,?)", order_items)

cursor.execute("""
CREATE TABLE CAMPAIGN (
    ID               INTEGER PRIMARY KEY,
    NAME             VARCHAR(100),
    CHANNEL          VARCHAR(20),
    BUDGET           REAL,
    START_DATE       DATE,
    END_DATE         DATE,
    LEADS_GENERATED  INTEGER,
    CONVERSIONS      INTEGER
)
""")

campaigns = [
    (1, "Spring Sale Blast",    "Email",  5000.00, "2024-03-01", "2024-03-31", 1200, 180),
    (2, "New Year Deals",       "Social", 8000.00, "2024-01-01", "2024-01-15",  950, 110),
    (3, "Google Search Q1",     "PPC",   12000.00, "2024-01-01", "2024-03-31", 3400, 420),
    (4, "Summer Fashion Drop",  "Social", 6500.00, "2024-06-01", "2024-06-30",  820,  95),
    (5, "Back to School",       "Email",  4200.00, "2024-08-01", "2024-08-31", 1050, 160),
    (6, "Electronics Weekend",  "PPC",    9000.00, "2024-04-05", "2024-04-07",  780, 230),
    (7, "Loyalty Rewards Push", "Email",  3000.00, "2024-05-01", "2024-05-15",  640,  98),
    (8, "Holiday Season Mega",  "Social",15000.00, "2024-11-25", "2024-12-25", 4200, 610),
]
cursor.executemany("INSERT INTO CAMPAIGN VALUES (?,?,?,?,?,?,?,?)", campaigns)

connection.commit()
print("sales.db created successfully.")
for table in ("CUSTOMER", "PRODUCT", "ORDERS", "ORDER_ITEM", "CAMPAIGN"):
    count = cursor.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"  {table}: {count} rows")
connection.close()
