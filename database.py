import sqlite3
from helpers import get_products, get_stock_count, parseXML, get_cateogry, get_availability
# from globals import products_required, manufacturers
import time
import datetime
import requests
import config
from flask import jsonify
import json
import math


def check_if_db_updated():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT updated_at FROM TABLES")  
    row = cur.fetchone()
    return row

def last_updated():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT updated_at, next_update_due FROM TABLES")  
    row = cur.fetchone()

    # updated_at = row["updated_at"]
    # updated_at_obj = datetime.datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S.%f")

    next_update_due = row["next_update_due"]
    next_update_due_obj = datetime.datetime.strptime(next_update_due, "%Y-%m-%d %H:%M:%S.%f")

    diff = next_update_due_obj - datetime.datetime.now()
    print(diff)
    total_minutes = math.ceil(diff.seconds/60)
    total_seconds = diff.seconds
    result = { "minutes": total_minutes, "seconds":total_seconds, "last_updated":row["updated_at"] }
    # date = row[0]
    # new_date_time = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    # print(new_date_time)
    # new_date_time = new_date_time.replace(minute=new_date_time.minute+5)
    # print(new_date_time)


    # list_row = list(row)
    # list_row.append(config.refresh_interval)
    # tuple_row = tuple(list_row)
    # print(f" row: {tuple_row}")
    # print(f" type: {type(tuple_row)}")
    # json_row = jsonify(tuple_row)
   
    return result

def create_table(con, name):
    # print("before create")
    con.execute(f"DROP TABLE IF EXISTS {name}")
    
    # print("dropped")
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
        # print("dropped")
    cur.execute('''
        CREATE TABLE tables (
            table_name TEXT,
            updating TEXT,
            updated_at TEXT,
            next_update_due
            )
            ''')
    print("tables table created")

    current_time = datetime.datetime.now()
    print(current_time.minute+config.refresh_interval_minutes)
    td = datetime.timedelta(minutes=+config.refresh_interval_minutes)
    next_update = current_time + td
    print(next_update)
    # next_update = current_time.replace(
    #     minute=current_time.minute+config.refresh_interval_minutes
    #     )

    cur.execute('''
    INSERT INTO tables 
        (table_name, updating, updated_at, next_update_due)
        VALUES (?, ?, ?, ?)''', 
        ("stock", "true", current_time, next_update) 
    )
    print("tables table updated")

    con.commit() 
    con.close()
    update_databse()


def get_info_for_table(category):

    con = sqlite3.connect('database.db')    
    cur = con.cursor()
    cur.execute(f"SELECT name, color, price, manufacturer, stock_status FROM stock WHERE type ='{category}'")  
    rows = cur.fetchall();  
    
    return rows


def update_databse():
    new_table_name = "new_table"
    con = sqlite3.connect('database.db')
    create_table(con, new_table_name)
    # try:
    print("new table created")
    cur = con.cursor()
    cur.execute('''UPDATE "tables"
        SET updating = "true"
        WHERE table_name = "stock"
        ''')
    print('tables table set to "updating"')


    # for product in products_required:
    #     print(f"retrieving json from api for {product}")
    s = requests.Session()
    json_data = get_cateogry(s)
    # print(f"retrieved json from api for {product}")
    
    a = time.perf_counter()
    # new_list = []
    # for j in json_data:
    #     for e in j:
    #         manufacturers.add(e["manufacturer"])
    #         new_list.append( (e["id"].upper(), e["type"], e["name"], e["color"][0],
    #             e["price"], e["manufacturer"]) )

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

    current_time = datetime.datetime.now()
    td = datetime.timedelta(minutes=+config.refresh_interval_minutes)
    next_update = current_time + td

    # next_update = current_time.replace(
    #     minute=current_time.minute+config.refresh_interval_minutes)

    cur.execute(f'''UPDATE "tables"
        SET 
        updating = "false",
        updated_at = "{current_time}",
        next_update_due = "{next_update}"

        WHERE table_name = "stock"
        ''')

    cur.execute("DROP TABLE IF EXISTS stock")
    cur.execute(f"ALTER TABLE {table_name} RENAME TO stock")

    con.commit() 
    con.close()