from datetime import datetime

class Transaction:
    def __init__(self,ID = None, date = None, description = None, amount = None, transaction_type = None, category = None):
        self._id = ID
        self._date = date
        self._description = description
        self._amount = amount
        self._transaction_type = transaction_type
        self._category = category

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, val):
        self._id = val
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self,val):
        self._date = val

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, val):
        self._amount = val

    @property
    def transaction_type(self):
        return self._transaction_type

    @transaction_type.setter
    def transaction_type(self, val):
        self._transaction_type = val

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, val):
        self._category = val