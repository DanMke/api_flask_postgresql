class PurchaseService:
    def __init__(self, database):
        self.database = database

    def get_purchases(self):
        query = "SELECT * FROM purchase"
        self.database.query(query)
        return self.database.cur.fetchall()

    def get_purchase_by_id(self, purchase_id):
        query = "SELECT * FROM purchase WHERE purchaseId = '{}'".format(purchase_id)
        self.database.query(query)
        return self.database.cur.fetchone()

    def create_purchase(self, purchase):
        # TODO SOH PODE VENDER SE TIVER DISC QUANTITY > 0
        query = "INSERT INTO purchase (purchaseDate, totalValue, email) VALUES ('{}', '{}', '{}')".format(purchase.purchase_datetime, purchase.total_value, purchase.email)
        self.database.query(query)
        self.database.commit()
        return self.database.cur.fetchone()

    def update_purchase_add_disc(self, purchase_id, disc_name, artist, quantity):
        query = "INSERT INTO has (purchaseId, discName, artist, quantity) VALUES ('{}', '{}', '{}', '{}')".format(purchase_id, disc_name, artist, quantity)
        self.database.query(query)
        self.database.commit()
        return self.database.cur.fetchone()

    def update_purchase_total_value(self, purchase_id, total_value):
        query = "UPDATE purchase SET totalValue = '{}' WHERE purchaseId = '{}'".format(total_value, purchase_id)
        self.database.query(query)
        self.database.commit()
        return self.database.cur.fetchone()