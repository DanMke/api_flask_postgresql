class Purchase:
    def __init__(self, purchaseDateTime, totalValue, email, effective=False, discs=[]):
        self.purchaseDateTime = purchaseDateTime
        self.totalValue = totalValue
        self.email = email
        self.effective = effective
        self.discs = discs
        self.purchaseId = None

    def __repr__(self):
        return "<Purchase {}>".format(self.purchase_id)