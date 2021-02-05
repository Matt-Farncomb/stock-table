
# Inventory Tracker

A simple site to view inventory information for a fictional warehouse. It follows the following steps:
1) A HTML diplsays a table with this data.
2) The backend retrieves inventory information from an API and then joins the data.
3) This retriveal is automated to take place every five minutes to coincide with the API, which is also updated at five minute intervals in a daemon on the backend.

## Technologies

* python 3.6
* flask
* sqlite
* javascript

## Usage
The vast majority of logic was handled in the python backend. In fact, JavaScipt is not even needed for this app to function and is used simply to have an interface that is more informative and to force a refresh on the browser  once the backend has finished updating, rather than at the interval set in `base.html`

### Backend
Visiting `https://bad-api-inventory.herokuapp.com/[category]` will return a html table of the inventory data for that particular category. On start-up, inventory data is retrieved from the "bad API".
There are three different GET requests that are made initially. One for each of the three product categories that this site tracks:
* [gloves](https://bad-api-assignment.reaktor.com/v2/products/gloves)
* [facemasks](https://bad-api-assignment.reaktor.com/v2/products/facemasks)
* [beanies](https://bad-api-assignment.reaktor.com/v2/products/beanies)

This JSON received is then stored in the database:
`database.db`

The names of the manufacturer's of the products (retrieved from the previous GET requests) are then used to get manufacturer info from the API with another GET request. For example:
* [umpante](https://bad-api-assignment.reaktor.com/v2/availability/umpante)
* [laion](https://bad-api-assignment.reaktor.com/v2/availability/laion)
* etc

Once that JSON is received it is joined up with the data already in the database.

The "bad API" is updated every five minutes so Python's AP Scheduler daemon is used to restart this backend process every five minutes ( interval defined in `config.py`).  All GET requests and parsing of data are handled in their own threads.

  ### Frontend
 The browser will check every five minutes to see if the DB has been updated. A counter is updated on the top of the screen indicating how long until the next update.
 If it has updated, JavaScript will force a refresh, returning the updated data.
If Javascript has been disabled, page will refresh every five minutes automatically thanks to this line:
`<meta  http-equiv="refresh"  content="{{ refresh_interval.seconds }}">`

  

## Why SQlite:

Sqlite is not the best option for Heroku as Heroku restarts the system once every 24hrs which would delete the Sqlite database file.

However, because the API updates every five minutes with fresh new data, the previous data becomes useless. So the database updater daemon rwipes and replaces the data  also on five minute intervals. Upon starting the app, it does a database update. So, considering the fact that this app takes no user data, no data that cannot be easily recovered is lost on cycling.

Therefore I felt Sqlite was sufficient for what was required.

NOTE: Another consideration would be the potential off-line time during the Heroku restart. Also, not really an issue. First of all. this app's start up time is very quick. Secondly, if this was an issue, with more expensive heroku accounts you can have preloading where the app will be booted up on another dyno a few seconds earlier so the transition between the two would be seamless.