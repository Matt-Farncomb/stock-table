

from flask import Flask
from database import initial_db_setup
from scheduler import begin_scheduler

print("you should see this only once")
app = Flask(__name__)
initial_db_setup()

# begin_scheduler()


import views

# if __name__ == "__main__":
#     app.run(debug=False)



