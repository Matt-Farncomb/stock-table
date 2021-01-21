from new_main import app
# from globals import products_required, table_headings
import config
from flask import render_template, jsonify
from database import get_info_for_table, check_if_db_updated

@app.route('/api')
def api():
    db_status = check_if_db_updated()
    return(jsonify(db_status))

@app.route('/')
def home():
    return products_table()

@app.route('/<category>')
def products_table(category=None):   
    if category == None:
        return product_not_found()
    if category not in config.products_required:
        return product_not_found(category)

    rows = get_info_for_table(category)

    products_remaining = [e for e in config.products_required if e != category]

    context = {
        "current_product": category,
        "products_required": products_remaining,
        "rows":rows,
        "headings":[ table.upper() for table in config.table_headings ]
    } 

    return render_template("table.html", **context)


def product_not_found(category=None):

    message = "Please select an option from above."

    if category == None:
        message = f"No product selected. {message}"
    else:
        message = f"A product called '{category}' could not be found.  {message}"

    context = {
        "message":message,
        "missing_category":category,
        "products_required": config.products_required,
        "headings": [ table.upper() for table in config.table_headings ]
    }

    return render_template("table.html", **context)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', products_required=config.products_required), 404