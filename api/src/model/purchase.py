class Purchase:
    def __init__(self, purchase_datetime, total_value, email):
        self.purchase_datetime = purchase_datetime
        self.total_value = total_value
        self.email = email

    def __repr__(self):
        return "<Purchase {}>".format(self.purchase_id)