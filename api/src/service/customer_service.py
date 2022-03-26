import json
from model.customer import Customer


class CustomerService:
    def __init__(self, database):
        self.database = database

    def get_customer_by_email(self, email):
        query = "SELECT * FROM customer WHERE email = '{}'".format(email)
        self.database.query(query)
        row = self.database.cur.fetchone()
        if row is None:
            return None
        customer = Customer(row[0], row[1], row[2],
                            row[3], row[4].isoformat(), row[5])
        return json.dumps(customer.__dict__)

    def get_customers(self):
        query = "SELECT * FROM customer"
        self.database.query(query)
        rows = self.database.cur.fetchall()
        if rows is None:
            return None
        customers = []
        for row in rows:
            customer = Customer(row[0], row[1], row[2],
                                row[3], row[4].isoformat(), row[5])
            customers.append(customer)
        return json.dumps([ob.__dict__ for ob in customers])

    def create_customer(self, customer):
        query = "INSERT INTO customer (email, fullName, phone, cpf, birthDate, active) VALUES ('{}', '{}', '{}', '{}', '{}', true)".format(
            customer.email, customer.full_name, customer.phone, customer.cpf, customer.birth_date)
        if customer.cpf is None:
            query = "INSERT INTO customer (email, fullName, phone, birthDate, active) VALUES ('{}', '{}', '{}', '{}', true)".format(
                customer.email, customer.full_name, customer.phone, customer.birth_date)
        self.database.query(query)
        self.database.commit()
        return json.dumps(customer.__dict__)

    def inactivate_customer(self, customer_email):
        query = "UPDATE customer SET active = false WHERE email = '{}'".format(
            customer_email)
        self.database.query(query)
        self.database.commit()
        if self.database.cur.rowcount == 0:
            return None
        return self.get_customer_by_email(customer_email)
