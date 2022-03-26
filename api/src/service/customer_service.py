from model.customer import Customer

class CustomerService:
    def __init__(self, database):
        self.database = database

    def get_customer_by_email(self, email):
        query = "SELECT email, fullName, phone, cpf, birthDate, active FROM customer WHERE email = '{}'".format(email)
        self.database.query(query)
        row = self.database.cur.fetchone()
        if row is None:
            return None
        customer = Customer(row[0], row[1], row[2],
                            row[3], row[4].isoformat(), row[5])
        return customer

    def get_customers(self):
        query = "SELECT email, fullName, phone, cpf, birthDate, active FROM customer"
        self.database.query(query)
        rows = self.database.cur.fetchall()
        if rows is None:
            return None
        customers = []
        for row in rows:
            customer = Customer(row[0], row[1], row[2],
                                row[3], row[4].isoformat(), row[5])
            customers.append(customer)
        return customers

    def create_customer(self, customer):
        query = "INSERT INTO customer (email, fullName, phone, cpf, birthDate, active) VALUES ('{}', '{}', '{}', '{}', '{}', true)".format(
            customer.email, customer.fullName, customer.phone, customer.cpf, customer.birthDate)
        if customer.cpf is None:
            query = "INSERT INTO customer (email, fullName, phone, birthDate, active) VALUES ('{}', '{}', '{}', '{}', true)".format(
                customer.email, customer.fullName, customer.phone, customer.birthDate)
        self.database.query(query)
        self.database.commit()
        return customer

    def inactivate_customer(self, customer_email):
        query = "UPDATE customer SET active = false WHERE email = '{}'".format(
            customer_email)
        self.database.query(query)
        self.database.commit()
        if self.database.cur.rowcount == 0:
            return None
        return self.get_customer_by_email(customer_email)

    def activate_customer(self, customer_email):
        query = "UPDATE customer SET active = true WHERE email = '{}'".format(
            customer_email)
        self.database.query(query)
        self.database.commit()
        if self.database.cur.rowcount == 0:
            return None
        return self.get_customer_by_email(customer_email)