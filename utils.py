import csv

import pandas as pd
from datetime import datetime
from TransactionSource import TransactionSource
from Transaction import Transaction
import os


class Tran:
    def __init__(self,date=None,description=None,amount=0,source=None):
        self.date = date
        self.description = description
        self.amount = amount
        self.source = source

    def __eq__(self, other):
        return (isinstance(other,Tran) and self.date == other.date and self.description == other.description and
                self.amount == other.amount and self.source == other.source)

    def __hash__(self):
        return hash(str(self.date)+self.description+str(self.amount)+self.source)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self,val):
        if isinstance(val,str):
            try:
                self._date = datetime.strptime(val,"%Y-%m-%d")
            except:
                raise Exception("Date Time Format Error in Import")
        elif isinstance(val,datetime):
            self._date = val

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self,val):
        self._description = val

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, val):
        self._amount = abs(val)

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, val):
        self._source = val


class Transactions():
    def __init__(self):
        self.trans = {}

    def add(self,date,description,amount,source):
        t = Tran(date=date,description=description,amount=amount,source=source)
        self.trans[t] = self.trans.get(t, 0) + 1

    def keys(self):
        return self.trans.keys()
    def values(self):
        return self.trans.values()

    def items(self):
        return self.trans.items()
    def get_value(self,key):
        if key not in self.trans.keys():
            raise KeyError
        else:
            return self.trans[key]

    def _lst_of_dict_add(self, transactions_lst, f_id = None):
        for t in transactions_lst:
            if f_id is None:
                self.add(date=t["date"], description=t["description"].stri(),
                         amount=float(t["amount"]), source=t["source"])
            else:
                try:
                    self.add(date=t["date"],description=(str(t["description"]).strip() + " " + str(t["sub-description"]).strip()).strip(),
                         amount=float(t["amount"]),source=f_id)
                except:
                    self.add(date=t["Date"], description=(str(t["Description"]).strip() + " " + str(t["Sub-description"]).strip()).strip(),
                             amount=float(t["Amount"]), source=f_id)
    def add_csv(self, file,f_id):
        with open(file, mode='r', encoding='utf-8') as f:
            csv_reader = csv.DictReader(f)
            transactions_lst = list(csv_reader)
        self._lst_of_dict_add(transactions_lst,f_id)

    def get_database(self):
        with Transaction() as t:
            transactions_lst = t.get_all()
        self._lst_of_dict_add(transactions_lst)

    def compare(self, other):
        assert isinstance(other, Transactions)
        result = Transactions()
        for t in self:
            if t in other:
                if self.trans[t] - other.trans[t] > 0:
                    result.add(date=t.date,description=t.description,amount=t.amount,source=t.souce)
                    result[t] = self.trans[t] - other.trans[t]
            else:
                result.add(date=t.date, description=t.description, amount=t.amount, source=t.souce)
        return result

    def add_to_database(self):
        t = Transaction()
        for count, trans in self.trans:
            for i in range(count):
                t.add(date=trans.date, description=trans.description, amount=trans.amount, source=trans.source)
        self.fill_unknown()

    def fill_unknown(self):
        pass





def bulk_import():
    with TransactionSource() as t:
        sources = t.get_all()
    for source in sources:
        for root, dirs, files in os.walk(source["folder_path"]):
            for file in files:
                if source["file_identifier"] in file:
                    if ".csv" in file:
                        new = Transactions()
                        new.add_csv(file,source["file_identifier"])
                    else: raise
                    existing = Transactions()
                    existing.get_database()
                    difference = new.compare(existing)
                    difference.add_to_database()



