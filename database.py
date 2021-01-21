import sqlite3
from helpers import get_products, get_stock_count, parseXML, get_cateogry, get_availability
# from globals import products_required, manufacturers
import time

import requests


def check_if_db_updated():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("SELECT updating FROM TABLES")  
    row = cur.fetchone()
    return row


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
            updating TEXT
            )
            ''')
    print("tables table created")

    cur.execute('''
    INSERT INTO tables 
        (table_name, updating)
        VALUES (?, ?)''', 
        ("stock", "true") 
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

    cur.execute(f'''UPDATE "tables"
        SET updating = "false"
        WHERE table_name = "stock"
        ''')

    cur.execute("DROP TABLE IF EXISTS stock")
    cur.execute(f"ALTER TABLE {table_name} RENAME TO stock")

    con.commit() 
    con.close()