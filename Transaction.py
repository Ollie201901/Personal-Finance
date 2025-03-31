from models import Transaction
class Transaction:
    def __init__(self, date, description, amount, transaction_type = None, category = None):
        self.date = date
        self.description = description
        self.amount = amount
        self.transaction_type = transaction_type
        self.category = category

    def __eq__(self, other):
        return self.date == other.date and self.description == other.description and self.amount == other.amount
