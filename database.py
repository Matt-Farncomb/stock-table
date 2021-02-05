import sqlite3
from helpers import get_products, get_stock_count, parseXML, get_cateogry, get_availability, next_update_time
import time
import datetime
import requests
import config
import json
import math
import logging

# returns a string of the last time the db was updated
def check_when_db_updated():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT updated_at FROM status")  
    row = cur.fetchone()
    return row[0]

# Return a dict containing when the db was last 
# updatded and how long ago
def last_updated():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT updated_at, next_update_due FROM status")  
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

# Create stock table and an index for it
def create_stock_table(con):
    con.execute("DROP TABLE IF EXISTS stock")
    
    con.execute('''
    CREATE TABLE stock (
        id TEXT, 
        type TEXT, 
        name TEXT, 
        color TEXT, 
        price TEXT, 
        manufacturer TEXT,
        stock_status TEXT DEFAULT 'REQUESTING...'
        )
        ''')
    con.execute("DROP INDEX IF EXISTS stock_index")
    con.execute("CREATE INDEX stock_index ON stock (id)")

# create status table to store update times
def create_status_table():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS status")
    cur.execute('''
        CREATE TABLE status (
            updated_at TEXT,
            next_update_due TEXT
            )
        ''')
    logging.info("Created 'status' Table")
    update_info = next_update_time()
  
    cur.execute('''
    INSERT INTO status 
        (updated_at, next_update_due)
        VALUES (?, ?)''', 
        (update_info["current_time"], update_info["next_update"]) 
    )
    logging.info("Updated 'status' Table")

    con.commit() 
    con.close()

    logging.info("Set up complete")

# return row from stock table of type category
def get_info_for_table(category):
    con = sqlite3.connect('database.db')    
    cur = con.cursor()
    cur.execute("SELECT name, color, price, manufacturer, stock_status FROM stock WHERE type =?", (category,))  
    rows = cur.fetchall();  
    return rows

# replace old stock table and insert new data retrieved from api
def update_databse():
    con = sqlite3.connect('database.db')
    create_stock_table(con)
    logging.info("Created 'stock' Table")
    cur = con.cursor()
    s = requests.Session()
    json_data = get_cateogry(s)
    a = time.perf_counter()

    cur.executemany(f'''
            INSERT INTO "stock" (id, type, name, color, price, manufacturer)
            VALUES 
            (? , ?, ?, ?, ?, ?)
    ''', json_data)

    b = time.perf_counter()
    logging.info(f"Stock data received and inserted in: {b - a} seconds")

    con.commit()    
    con.close()

    update_stock_count(s)

# updates the stock status of products in the database
def update_stock_count(session):
    con = sqlite3.connect('database.db')
    cur = con.cursor()

    a = time.perf_counter() 

    xml_data = get_availability(session)

    cur.executemany('''
        UPDATE stock
        SET stock_status = ?
        WHERE id = ?
        ''', xml_data) 

    update_info = next_update_time()

    cur.execute('''UPDATE status
        SET updated_at = ?, next_update_due = ?''',
        (update_info["current_time"], update_info["next_update"])
    )

    b = time.perf_counter() 
    logging.info(f"Manufacturer data received and inserted in: {b - a} seconds")

    con.commit() 
    con.close()