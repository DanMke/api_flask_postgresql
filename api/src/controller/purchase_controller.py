from flask import jsonify, request, json

from datetime import datetime

from model.purchase import Purchase
from service.purchase_service import PurchaseService
from service.disc_service import DiscService

class PurchaseController:
    def __init__(self, app, database):
        self.app = app
        self.purchase_service = PurchaseService(database)
        self.disc_servcice = DiscService(database)

    def routes(self):
        @self.app.route('/purchases', methods=['GET'])
        def get_purchases():
            purchases = self.purchase_service.get_purchases()
            return jsonify(purchases), 200

        @self.app.route('/purchases/<purchase_id>', methods=['GET'])
        def get_purchase(purchase_id):
            purchase = self.purchase_service.get_purchase_by_id(purchase_id)
            return jsonify(purchase), 200

        @self.app.route('/purchases', methods=['POST'])
        def create_purchase():
            purchase = Purchase(datetime.now(), 0.0, request.json['email'])
            discs = []
            total_value = 0.0
            for disc in request.json['discs']:
                self.purchase_service.update_purchase_add_disc(purchase['purchase_id'], disc['disc_name'], disc['artist'], disc['quantity'])
                disc_db = self.disc_servcice.get_disc_by_artist_and_name(disc['artist'], disc['name'])
                discs.append(disc_db)
                total_value += disc_db.unitary_value * disc['quantity']
            self.purchase_service.update_purchase_total_value(purchase['purchase_id'], total_value)
            return jsonify(purchase), 201