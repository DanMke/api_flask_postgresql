class Customer:
    def __init__(self, email, full_name, phone, cpf, birth_date, active):
        self.email = email
        self.full_name = full_name
        self.phone = phone
        self.cpf = cpf
        self.birth_date = birth_date
        self.active = active

    def __repr__(self):
        return "<Customer {}>".format(self.name)