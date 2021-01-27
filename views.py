from main import app
# from globals import products_required, table_headings
import config
from flask import render_template, jsonify
from database import get_info_for_table, check_if_db_updated, last_updated

@app.route('/api')
def api():
    db_status = check_if_db_updated()
    return(jsonify(db_status))

@app.route('/')
@app.route('/<category>')
def products_table(category=None):

    refresh = last_updated()

    context = {
        "headings":[ table.upper() for table in config.table_headings ],
        "refresh_interval": {
            "seconds": refresh["seconds"],
            "minutes": refresh["minutes"],
            "last_updated": refresh["last_updated"]
        }
    } 
    # valid category
    if category in config.products_required:
        products_remaining = [e for e in config.products_required if e != category]
        context["current_product"] = category
        context["products_required"] = products_remaining
        context["rows"] = get_info_for_table(category)
    # not a valid category
    else:
        message = "Please select an option from above."
        if category == None:
            message = f"No product selected. {message}"
        elif category not in config.products_required:
            message = f"A product called '{category}' could not be found.  {message}"
        context["message"] = message
        context["products_required"] = config.products_required
    
    return render_template("table.html", **context)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', products_required=config.products_required), 404