import xml.etree.ElementTree as et
import json
import threading
import config
import datetime
import logging
import requests 

def parseXML(xml):
    root = et.fromstring(xml)
    for child in root:
        if child.tag == "INSTOCKVALUE":
            return child.text 

# Retrieve JSON from url
# IF request fails, try again
def get_json(url_end, session):

    url = "https://bad-api-assignment.reaktor.com/v2/" + url_end
    response = session.get(url)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logging.warning(e)
        return False

    header = response.headers
    logging.info(f"retrieved: {url_end}")
    error_key = "X-Error-Modes-Active"      
    if header["Content-Length"] == "0":
        logging.warning(f"Category named '{url_end}' no longer available")
        return False
    elif error_key in header:
        if header[error_key] ==  "availability-empty":
            logging.warning(f"Error in accessing {url_end} API. Trying again...")
            return get_json(url_end, session)
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
        if products != False:
            for e in products:
                config.manufacturers.add(e["manufacturer"])
                results.append( (e["id"].upper(), e["type"], e["name"], e["color"][0],
                    e["price"], e["manufacturer"]) )

    return spawn_threads(config.products_required, session, get_all_products)


def get_availability(session):

    def get_all_stock(manufacturer, results):
        stock_count = get_stock_count(manufacturer, session)
        if stock_count != False:
            for x in stock_count:
                results.append((parseXML(x["DATAPAYLOAD"]), x["id"]))
    
    return spawn_threads(config.manufacturers, session, get_all_stock)

# Return the next time the scheduler will run and how many seconds from now that will be
def next_update_time():
    current_time = datetime.datetime.now()
    td = datetime.timedelta(minutes=+config.refresh_interval_minutes)
    next_update = current_time + td
    update_dict = { "current_time":current_time, "next_update":next_update }
    return update_dict