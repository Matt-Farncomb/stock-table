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


# def get_stock_count2(manufacturers, session):
#     results = []    

#     def get_all_stock(manufacturer):
#         stock_count = get_stock_count(manufacturer, session)
#         for x in stock_count:
#             results.append((parseXML(x["DATAPAYLOAD"]), x["id"]))


#     threads = [ run_thread(get_all_stock, x) for x in manufacturers ]

#     # We now pause execution on the main thread by 'joining' all of our started threads.
#     # This ensures that each has finished processing the urls.
#     for thread in threads:
#         thread.join()

#     return results
    
# def get_products2(products_required, manufacturers, session):
    
#     results = []
    
#     def get_all_products(products_required):
#         products = get_products(products_required, session)
#         for e in products:
#             manufacturers.add(e["manufacturer"])
#             results.append( (e["id"].upper(), e["type"], e["name"], e["color"][0],
#                 e["price"], e["manufacturer"]) )
#         # results.append(products)
    
#     threads = [ run_thread(get_all_products, x) for x in products_required ]

#     for thread in threads:
#         thread.join()

#     return results