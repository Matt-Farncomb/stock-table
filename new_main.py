

from flask import Flask
from database import initial_db_setup
from scheduler import begin_scheduler
# import time

# if __name__ == "__main__":
print("you should see this only once")
app = Flask(__name__)
# initial_db_setup()

# begin_scheduler()


import views

# if __name__ == "__main__":
#     app.run(debug=False)


# @app.route('/<category>')
# def hello_world(category):

#     con = sqlite3.connect('database.db')    
#     cur = con.cursor()

#     # cur.execute("SELECT name FROM tables WHERE active ='true'")  

#     # current_table = cur.fetchone()
#     # try:
#     cur.execute(f"SELECT name, color, price, manufacturer, stock_status FROM stock WHERE type ='{category}'")  
#     # except:
#     #     time.sleep(.5)
#     #     # wait 0.25 seconds then (wait until stock is renamed)
#     #     return hello_world(category)

#     rows = cur.fetchall();  
#     # print(rows)

#     context = {
#         "products_required": products_required,
#         "rows":rows,
#         "headings":[ table.upper() for table in table_headings ]
#     } 
   
    
#     return render_template("table.html", **context)

# def create_table(con, name):
#     # print("before create")
#     con.execute(f"DROP TABLE IF EXISTS {name}")
#     # print("dropped")
#     con.execute(f'''
#     CREATE TABLE "{name}" (
#         id TEXT, 
#         type TEXT, 
#         name TEXT, 
#         color TEXT, 
#         price TEXT, 
#         manufacturer TEXT,
#         stock_status TEXT DEFAULT OUTOFSTOCK
#         )
#         ''')

# def update_databse(products_required, manufacturers):
#     new_table_name = "new_table"
#     con = sqlite3.connect('database.db')
#     create_table(con, new_table_name)
#     # try:
#     print("new table created")
#     cur = con.cursor()
#     cur.execute('''UPDATE "tables"
#         SET updating = "true"
#         WHERE table_name = "stock"
#         ''')
#     print('tables table set to "updating"')
#     for product in products_required:
#         ("retrieving json from api for product")
#         json_data = get_products(product)
#         ("retrieved json from api for product")
#         for e in json_data:
#             manufacturers.add(e["manufacturer"])
#             cur.execute(f'''
#                 INSERT INTO "{new_table_name}" 
#                     (id, type, name, color, price, manufacturer)
#                     VALUES (?, ?, ?,
#                     ?, ?, ?)''', 
#                     (e["id"].upper(), e["type"], e["name"], e["color"][0],
#                     e["price"], e["manufacturer"]) 
#                 )
    
#     con.commit() 
#     # print(rows)
#     con.close()
#     print("table updated with main info")
#     update_stock_count(manufacturers, new_table_name)
#     # print("here") 
  
       
# def get_json(url_end):
#     url = "https://bad-api-assignment.reaktor.com/v2/" + url_end
#     response = requests.request("GET", url)
#     # print(url_end)

#     # print("https://bad-api-assignment.reaktor.com/v2/" + url_end)
#     json_data = response.json()
   
#     return json_data


# def get_products(product):
#     return get_json("products/" + product)
#     # print(json)
#     # if json["code"] == 200:
#     #     print("is 200")
#     #     return json["response"]
 

# def get_stock_count(manufacturer):
#     json = get_json("availability/" + manufacturer)
#     # print(json)
#     if json["code"] == 200:
#         # print("is 200")
#         return json["response"]

# def parseXML(xml):
#     # root = ET.fromstring(xml_string)
#     # tree =  et.parse(xml)
#     root = et.fromstring(xml)
#     # root = tree.getroot()
#     for child in root:
#         if child.tag == "INSTOCKVALUE":
#             # print(child.text)
#             return child.text 

# def update_stock_count(manufacturers, table_name):
#     con = sqlite3.connect('database.db')
#     cur = con.cursor()
#     for manufacturer in manufacturers:
#         # print(manufacturer)
#         print("retrieving json from api for manufacturer")
#         stock_count = get_stock_count(manufacturer)
#         print("retrieved json from api for manufacturer")
#         # print(stock_count)
#         if stock_count[0] != None:
#             json_data = stock_count
#             # print(type(manufacturer))
#             for j in json_data:
#                 # ids.add(json["id"])
#                 if not isinstance(j, str):
#                     # print(j)
#                     # print(type(j))
#                     _id = j["id"]
#                     # print(_id)
#                     status = parseXML(j["DATAPAYLOAD"])
#                     # print(_id)
#                     # print(status)
#                     # cur.execute(f"SELECT * FROM stock")
#                     # print(cur.fetchall())
#                     # print(j)
                 
#                     cur.execute(f'''
#                         UPDATE {table_name}
#                         SET stock_status = "{status}"
#                         WHERE id = "{_id}"
#                         ''')

#     # cur.exec('''
#     #     CREATE UNIQUE INDEX stuff 
#     #     ON new_table (type)
#     # ''')

#     # curr.exec('''
#     # ALTER TABLE existing_table
#     # RENAME TO new_table;
#     # ''')
#     print("stock count inserted")
#     cur.execute(f'''UPDATE "tables"
#         SET updating = "false"
#         WHERE table_name = "stock"
#         ''')
#     cur.execute("DROP TABLE IF EXISTS stock")
#     print("stock table droppped")
#     cur.execute(f"ALTER TABLE {table_name} RENAME TO stock")
#     print(f"{table_name} renamed to stock")

#     con.commit() 
#     con.close()
            
    


# def background_db_updater():
#     print("Scheduler is alive!")
#     update_databse(products_required, manufacturers)
#     print("database updated")


# def initial_db_setup():
#     con = sqlite3.connect('database.db')
#     cur = con.cursor()
#     create_table(con, "stock")
#     cur.execute("DROP TABLE IF EXISTS tables")
#         # print("dropped")
#     cur.execute('''
#         CREATE TABLE tables (
#             table_name TEXT,
#             updating TEXT
#             )
#             ''')
#     print("tables table created")

#     cur.execute('''
#     INSERT INTO tables 
#         (table_name, updating)
#         VALUES (?, ?)''', 
#         ("stock", "true") 
#     )
#     print("tables table updated")

#     con.commit() 
#     con.close()
#     update_databse(products_required, manufacturers)

# def begin_scheduler():
#     sched = BackgroundScheduler(daemon=True)
#     sched.add_job(background_db_updater,'interval',minutes=3)
#     sched.start()
#     print("Schedule initiated")
 



# begin_scheduler()





