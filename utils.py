import csv

import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import database as db
import os

def bulk_import():
    with db.TransactionSource() as t:
        sources = t.get_all()
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
                        trans["date"] = datetime.strptime(transaction["Date"], '%Y-%m-%d').date()
                        trans["description"] = transaction["Description"] + " " + transaction["Sub-description"]
                        trans["amount"] = abs(float(transaction["Amount"]))
                        trans["source"] = source["file_identifier"]
                        new.append(trans)
                    old = db.Transaction().get_all()
                    new = transform(new)
                    old = transform(old)
                    difference = compare(new,old)
                    for trans, num in difference.items():
                        with db.Transaction() as t:
                            t.add(date=trans["date"],description=trans["description"],amount=trans["amount"],
                                             source=trans["source"])#,transaction_type=,category=)


def transform(file):
    result = {}
    for row in file:
        result[row] = result.get(row, 0) + 1
    return result

def compare(new, old):
    result = {}
    for trans in new:
        if trans in old:
            if new[trans] > old[trans]:
                result[trans] = old[trans] - new[trans]
        else:
            result[trans] = 1
    return result
