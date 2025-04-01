import csv

import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import database as db
import os

def bulk_import():
    sources = db.TransactionSource().get_all()
    for source in sources:
        for root, dirs, files in os.walk(source["folder_path"]):
            for file in files:
                if source["file_identifier"] in file:
                    if ".csv" in file:
                        with open(file, mode='r', encoding='utf-8') as f:
                            csv_reader = csv.DictReader(f)
                            transactions_lst = list(csv_reader)
                    elif ".xlsx" in file:
                        df = pd.read_excel(file)
                        transactions_lst = df.to_dict(orient='records')
                    new = []
                    for transaction in transactions_lst:
                        trans = {}
                        trans["date"] = datetime.strptime(new_transaction["Date"], '%Y-%m-%d').date()
                        trans["description"] = new_transaction["Description"] + " " + transaction["Sub-description"]
                        trans["amount"] = abs(float(new_transaction["Amount"]))
                        trans["source"] = source["file_identifier"]
                        new.append(trans)
                    old = db.Transaction().get_all()
                    difference = compare(new,old)




def compare(new_transaction, old_transaction):
    result =
    for transaction in new_transaction:
        if transaction in old_transaction:
            if new_transaction[transaction] > old_transaction[transaction]:
                result[transaction] = old_transaction[transaction] - new_transaction[transaction]
        else:
            result[transaction] = 1
    return result