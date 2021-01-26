import xml.etree.ElementTree as et
import json
import requests
import time
import threading
# from config import products_required, manufacturers
import config

def parseXML(xml):
    root = et.fromstring(xml)
    for child in root:
        if child.tag == "INSTOCKVALUE":
            return child.text 


def get_json(url_end, session):
    print(f"retrieving: {url_end}")

    url = "https://bad-api-assignment.reaktor.com/v2/" + url_end
    response = session.get(url)
    # print(url_end)
    header = response.headers
    print(f"retrieved: {url_end}")
    error_key = "X-Error-Modes-Active"
    if error_key in header:
        if header[error_key] ==  "availability-empty":
            print(f"Error in accessing {url_end} API. Trying again...")
            return get_json(url_end, session)
    # print("https://bad-api-assignment.reaktor.com/v2/" + url_end)
    json_data = response.json()
   
    return json_data


def get_products(product, session):
    return get_json("products/" + product, session)


def get_stock_count(manufacturer, session):
    json = get_json("availability/" + manufacturer, session)
    return json["response"]


def run_thread(func, arg, results):
    thread = threading.Thread(target=func, args=[arg, results])
    thread.start()
    return thread


def spawn_threads(url_param, session, func):
    results = []
    threads = [ run_thread(func, x, results) for x in url_param ]
    for thread in threads:
        thread.join()

    return results


def get_cateogry(session):

    def get_all_products(product, results):
        products = get_products(product, session)
        for e in products:
            config.manufacturers.add(e["manufacturer"])
            results.append( (e["id"].upper(), e["type"], e["name"], e["color"][0],
                e["price"], e["manufacturer"]) )

    return spawn_threads(config.products_required, session, get_all_products)


def get_availability(session):

    def get_all_stock(manufacturer, results):
        stock_count = get_stock_count(manufacturer, session)
        for x in stock_count:
            results.append((parseXML(x["DATAPAYLOAD"]), x["id"]))
    
    return spawn_threads(config.manufacturers, session, get_all_stock)


# def append_to_json(row):
#     json_row = jsonify(row)
#     refresh_interval = { "refresh_interval": config.refresh_interval }
#     x = json_row.update(refresh_interval)