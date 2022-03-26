from flask import Flask

from database import Database

from controller.customer_controller import CustomerController
from controller.disc_controller import DiscController
from controller.purchase_controller import PurchaseController

app = Flask(__name__)
app.config['DEBUG'] = True

database = Database()

customer_controller = CustomerController(app, database)
disc_controller = DiscController(app, database)
purchase_controller = PurchaseController(app, database)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)