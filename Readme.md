# Inventory Tracker
A simple site to view inventory information for a fictional warehouse.
The HTML diplsays a table with this data.
The backend retrieves inventory information from a poorly designed API and then joins the data
in a logical way.
This retriveal is automated to take place every five minutes to coincide with the API,
which is also updated at five minute intervals.

## Technologies

* python 3.6
* flask
* sqlite
* javascript

## Usage
Visiting "url/category" will return a html table of the inventory data for that particular category.

On start-up, inventory data is retrieved from the "bad API".
There are three different GET requests that are made initially.
One for each of the three product categories that this site tracks: gloves, facemasks and beanies.
This JSON received is then stored in the database.

The manufacturer's names of the products is then used to get manufacturer info from the API.
Once that JSON is received it is joined up with the data already in the database.
The API is updated every five minutes so Python's AP Scheduler is used to re-retrieve the data from the API every five minutes.
Each request and db update is run in it's own thread.

The client will check every five minutes to see if the DB has been updated.
If it has, JavaScript will force a refresh, returning the updated data.
If Javascript has been disabled, page will refresh every five minutes without confirmation.



