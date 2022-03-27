from flask import jsonify, request
import json
import pytz
from datetime import datetime

from model.purchase import Purchase
from service.purchase_service import PurchaseService
from service.disc_service import DiscService

class PurchaseController:
    def __init__(self, app, database):
        self.app = app
        self.purchase_service = PurchaseService(database)
        self.disc_service = DiscService(database)
        self.routes()

    def routes(self):
        @self.app.route('/purchases', methods=['GET'])
        def get_purchases():
            args = request.args
            purchases = self.purchase_service.get_purchases(args.to_dict())
            if purchases is None:
                return [], 200
            return json.dumps([ob.__dict__ for ob in purchases]), 200

        @self.app.route('/purchases/<purchaseId>', methods=['GET'])
        def get_purchase(purchaseId):
            purchase = self.purchase_service.get_purchase_by_id(purchaseId)
            if purchase is None:
                return jsonify({'message': 'Purchase not found'}), 404
            return json.dumps(purchase.__dict__), 200

        @self.app.route('/purchases', methods=['POST'])
        def create_purchase():
            if not request.json:
                return jsonify({'message': 'No data provided'}), 400
            elif (
                'email' not in request.json or 'discs' not in request.json or
                not request.json['email'] or not request.json['discs']
            ):
                return jsonify({'message': 'Email of Customer and Discs are required'}), 400

            discs = []
            purchase = Purchase(str(datetime.now(pytz.timezone("America/Sao_Paulo"))), 0.0, request.json['email'], False, discs)
            purchaseId = self.purchase_service.create_purchase(purchase)

            if purchaseId is None:
                return jsonify({'message': 'Purchase not created, Customer not found'}), 400

            if len(request.json['discs']) == 0:
                return jsonify({'message': 'Purchase not effective, no discs found'}), 400

            total_value = 0.0
            for disc in request.json['discs']:
                disc_db = self.disc_service.get_disc_by_artist_and_name(disc['artist'], disc['discName'])

                if disc_db is None:
                    return jsonify({'message': 'Disc {} by {} not found'.format(disc['discName'], disc['artist'])}), 400

                total_value += disc_db.unitaryValue * disc['quantity']
                self.purchase_service.update_purchase_add_disc(purchaseId, disc['discName'], disc['artist'], disc['quantity'])
                discs.append(disc)

                if disc_db.availableQuantity < disc['quantity']:
                    return jsonify({'message': 'Disc {} by {} not available'.format(disc['discName'], disc['artist'])}), 400

            for disc in request.json['discs']:
                self.disc_service.update_disc_quantity(disc['artist'], disc['discName'], disc['quantity'])

            self.purchase_service.update_purchase_total_value(purchaseId, total_value)
            self.purchase_service.update_purchase_effective(purchaseId)

            purchase.purchaseId = purchaseId
            purchase.discs = discs
            purchase.totalValue = total_value
            purchase.effective = True

            return json.dumps(purchase.__dict__), 201