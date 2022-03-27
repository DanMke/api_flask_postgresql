from flask import jsonify, request
import json
from model.customer import Customer
from service.customer_service import CustomerService
class CustomerController:
    def __init__(self, app, database):
        self.app = app
        self.customer_service = CustomerService(database)
        self.routes()

    def routes(self):
        @self.app.route('/', methods=['GET'])
        def index():
            return jsonify({'message': 'Welcome to Lea Record Shop!'}), 200

        @self.app.route('/customers', methods=['GET'])
        def get_customers():
            customers = self.customer_service.get_customers()
            if customers is None:
                return [], 200
            return json.dumps([ob.__dict__ for ob in customers]), 200

        @self.app.route('/customers/<customer_email>', methods=['GET'])
        def get_customer(customer_email):
            customer = self.customer_service.get_customer_by_email(
                customer_email)
            if customer is None:
                return jsonify({'message': 'Customer not found'}), 404
            return json.dumps(customer.__dict__), 200

        @self.app.route('/customers', methods=['POST'])
        def create_customer():
            if not request.json:
                return jsonify({'message': 'No data provided'}), 400
            elif (
                'email' not in request.json or 'fullName' not in request.json or 
                'phone' not in request.json or 'birthDate' not in request.json or 
                not request.json['email'] or not request.json['fullName'] or 
                not request.json['phone'] or not request.json['birthDate']
            ):
                return jsonify({'message': 'Email, Full Name, Phone and Birth Date are required'}), 400
            customer = self.customer_service.get_customer_by_email(request.json['email'])
            if customer:
                if not customer.active:
                    customer = self.customer_service.activate_customer(request.json['email'])
                    return json.dumps(customer.__dict__), 201
                else:
                    return jsonify({'message': 'Customer already exists'}), 409

            customer = Customer(request.json['email'], request.json['fullName'],
                                request.json['phone'], request.json['cpf'], request.json['birthDate'], True)
            customer = self.customer_service.create_customer(customer)
            return json.dumps(customer.__dict__), 201

        @self.app.route('/customers/<customer_email>', methods=['PUT'])
        def inactivate_customer(customer_email):
            customer = self.customer_service.inactivate_customer(
                customer_email)
            if customer is None:
                return jsonify({'message': 'Customer not found'}), 404
            return json.dumps(customer.__dict__), 200
