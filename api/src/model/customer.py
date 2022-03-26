class Customer:
    def __init__(self, email, fullName, phone, cpf, birthDate, active):
        self.email = email
        self.fullName = fullName
        self.phone = phone
        self.cpf = cpf
        self.birthDate = birthDate
        self.active = active

    def __repr__(self):
        return "<Customer {}>".format(self.name)