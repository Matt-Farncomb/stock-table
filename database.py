import sqlite3
from helpers import get_products, get_stock_count, parseXML, get_cateogry, get_availability, next_update_time
import time
import datetime
import requests
import config
import json
import math


def check_when_db_updated():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT updated_at FROM TABLES")  
    row = cur.fetchone()
    return row

# Return a dict containing when the db was last 
# updatded and how long ago
def last_updated():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT updated_at, next_update_due FROM TABLES")  
    row = cur.fetchone()

    next_update_due = row["next_update_due"]
    next_update_due_obj = datetime.datetime.strptime(
        next_update_due, "%Y-%m-%d %H:%M:%S.%f")

    diff = next_update_due_obj - datetime.datetime.now()

    total_minutes = math.ceil(diff.seconds/60)
    total_seconds = diff.seconds
    result = { 
        "minutes": total_minutes, 
        "seconds":total_seconds, 
        "last_updated":row["updated_at"] 
        }

    return result

def create_table(con, name):
    con.execute(f"DROP TABLE IF EXISTS {name}")
    
    con.execute(f'''
    CREATE TABLE "{name}" (
        id TEXT, 
        type TEXT, 
        name TEXT, 
        color TEXT, 
        price TEXT, 
        manufacturer TEXT,
        stock_status TEXT DEFAULT OUTOFSTOCK
        )
        ''')
    con.execute(f"DROP INDEX IF EXISTS {name}_index")
    con.execute(f"CREATE INDEX {name}_index ON {name} (id)")

def initial_db_setup():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    create_table(con, "stock")
    cur.execute("DROP TABLE IF EXISTS tables")
    cur.execute('''
        CREATE TABLE tables (
            table_name TEXT,
            updating TEXT,
            updated_at TEXT,
            next_update_due
            )
            ''')
    print("tables table created")

    update_info = next_update_time()
  
    cur.execute('''
    INSERT INTO tables 
        (table_name, updating, updated_at, next_update_due)
        VALUES (?, ?, ?, ?)''', 
        ("stock", "true", update_info["current_time"], update_info["next_update"]) 
    )
    print("tables table updated")

    con.commit() 
    con.close()
    update_databse()


def get_info_for_table(category):

    con = sqlite3.connect('database.db')    
    cur = con.cursor()
    cur.execute("SELECT name, color, price, manufacturer, stock_status FROM stock WHERE type =?", (category,))  
    rows = cur.fetchall();  
    
    return rows


def update_databse():
    new_table_name = "new_table"
    con = sqlite3.connect('database.db')
    create_table(con, new_table_name)
    print("new table created")
    cur = con.cursor()
    cur.execute('''UPDATE "tables"
        SET updating = "true"
        WHERE table_name = "stock"
        ''')
    print('tables table set to "updating"')

    s = requests.Session()
    json_data = get_cateogry(s)
    a = time.perf_counter()

    cur.executemany(f'''
            INSERT INTO "{new_table_name}" (id, type, name, color, price, manufacturer)
            VALUES 
            (? , ?, ?, ?, ?, ?)
    ''', json_data)
    b = time.perf_counter()
    print(f"Time took {b - a} seconds")

    con.commit() 
    con.close()
    print("table updated with main info")
    update_stock_count(new_table_name, s)


def update_stock_count(table_name, session):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    a = time.perf_counter() 

    xml_data = get_availability(session)

    # xml_data = [(parseXML(x["DATAPAYLOAD"]), x["id"]) 
    # for row in get_stock_count2(manufacturers, s)
    #     for x in row
    #         ]

    b = time.perf_counter() 

    print(f"Time for nested list comp took {b - a} seconds")

    cur.executemany(f'''
        UPDATE {table_name}
        SET stock_status = ?
        WHERE id = ?
        ''', xml_data) 

    update_info = next_update_time()

    cur.execute(f'''UPDATE "tables"
        SET 
        updating = "false",
        updated_at = "{update_info["current_time"]}",
        next_update_due = "{update_info["next_update"]}"

        WHERE table_name = "stock"
        ''')

    cur.execute("DROP TABLE IF EXISTS stock")
    cur.execute(f"ALTER TABLE {table_name} RENAME TO stock")

    con.commit() 
    con.close()