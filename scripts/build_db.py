import sqlite3, csv, os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(SCRIPT_DIR, "..")
DATA_DIR = os.path.join(ROOT, "data")

conn = sqlite3.connect(os.path.join(DATA_DIR, "walmart_project.db"))
cur = conn.cursor()
cur.executescript("""
DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    store_id INTEGER,
    date TEXT,
    week_of_year INTEGER,
    year INTEGER,
    weekly_sales REAL,
    holiday_flag INTEGER,
    temperature REAL,
    fuel_price REAL,
    cpi REAL,
    unemployment REAL
);
""")

rows = []
with open(os.path.join(DATA_DIR, "Walmart.csv")) as f:
    for r in csv.DictReader(f):
        d = datetime.strptime(r["Date"], "%d-%m-%Y")
        rows.append((
            int(r["Store"]), d.strftime("%Y-%m-%d"), d.isocalendar()[1], d.year,
            float(r["Weekly_Sales"]), int(r["Holiday_Flag"]),
            float(r["Temperature"]), float(r["Fuel_Price"]),
            float(r["CPI"]), float(r["Unemployment"])
        ))

cur.executemany("INSERT INTO sales VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
cur.execute("CREATE INDEX idx_store ON sales(store_id)")
cur.execute("CREATE INDEX idx_date ON sales(date)")
conn.commit()
conn.close()
print(f"Loaded {len(rows)} rows -> walmart_project.db")
