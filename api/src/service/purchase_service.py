from model.purchase import Purchase
from service.customer_service import CustomerService
class PurchaseService:
    def __init__(self, database):
        self.database = database
        self.customer_service = CustomerService(database)

    def get_purchases(self):
        query = "SELECT purchaseId, purchaseDateTime, totalValue, email, effective FROM purchase"
        self.database.query(query)
        return self.database.cur.fetchall()

    def get_purchase_by_id(self, purchaseId):
        query = "SELECT purchaseId, purchaseDateTime, totalValue, email, effective FROM purchase WHERE purchaseId = '{}'".format(purchaseId)

        self.database.query(query)
        row = self.database.cur.fetchone()
        if row is None:
            return None
        purchase = Purchase(row[1].isoformat(), row[2], row[3], row[4])
        purchase.purchaseId = row[0]

        query = "SELECT purchaseId, discname, artist, quantity FROM has WHERE purchaseId = '{}'".format(purchaseId)
        self.database.query(query)
        discs = []
        rows = self.database.cur.fetchall()
        for row in rows:
            discs.append({
                'discName': row[1],
                'artist': row[2],
                'quantity': row[3]
            })
        purchase.discs = discs
        return purchase

    def create_purchase(self, purchase):
        customer = self.customer_service.get_customer_by_email(purchase.email)
        if customer is None:
            return None
        query = "INSERT INTO purchase (purchaseDateTime, totalValue, email, effective) VALUES ('{}', '{}', '{}', false) RETURNING purchaseId".format(purchase.purchaseDateTime, purchase.totalValue, purchase.email)
        self.database.query(query)
        self.database.commit()
        purchaseId = self.database.cur.fetchone()[0]
        return purchaseId

    def update_purchase_add_disc(self, purchaseId, discName, artist, quantity):
        query = "INSERT INTO has (purchaseId, discName, artist, quantity) VALUES ('{}', '{}', '{}', '{}')".format(purchaseId, discName, artist, quantity)
        self.database.query(query)
        self.database.commit()
        return

    def update_purchase_total_value(self, purchaseId, totalValue):
        query = "UPDATE purchase SET totalValue = '{}' WHERE purchaseId = '{}'".format(totalValue, purchaseId)
        self.database.query(query)
        self.database.commit()
        return self.get_purchase_by_id(purchaseId)

    def update_purchase_effective(self, purchaseId):
        query = "UPDATE purchase SET effective = true WHERE purchaseId = '{}'".format(purchaseId)
        self.database.query(query)
        self.database.commit()
        return self.get_purchase_by_id(purchaseId)

    # TODO: cancel purchase