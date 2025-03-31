import csv

import pandas as pd
from openpyxl import load_workbook
import io
from datetime import datetime
from Transaction import Transaction
from models import Transaction as mTransaction

def process_CSV(file, filename):
    with open(file, mode = 'r', encoding = 'utf-8') as f:
        csv_reader = csv.DictReader(f)
        transactions_lst = list(csv_reader)
    return process_transactions(transactions_lst,filename)

def process_xls(file, filename):
    df = pd.read_excel(file)
    transactions_lst = df.to_dict(orient='records')
    return process_transactions(transactions_lst,filename)

def process_transactions(transactions_lst,filename):
    transactions = {}
    for transaction in transactions_lst:
        date = datetime.strptime(transaction["Date"], '%Y-%m-%d').date()
        description = transaction["Description"] + " " + transaction["Sub-description"]
        if 'visa' in filename:
            amount = float(transaction["Amount"])
            if amount >= 0.:
                transaction_type = "Expense"
            else:
                transaction_type = "Transfer"
            amount = abs(amount)

        else:
            amount = float(transaction["Amount"])
            if amount >= 0.:
                transaction_type = "Income"
            else:
                transaction_type = "Expense"
            amount = abs(amount)
        trans = Transaction(date=date, description=description, amount=amount, transaction_type=transaction_type)
        if trans in transactions:
            transactions[trans] += 1
        else:
            transactions[trans] = 1
    return transactions

def get_all_db_transactions():
    transactions = {}
    for transaction in mTransaction.query.all():
        trans = Transaction(date=transaction.date, description=transaction.description,
                            amount=transaction.amount, transaction_type=transaction.transaction_type_id)
        if trans in transactions:
            transactions[trans] += 1
        else:
            transactions[trans] = 1
    return transactions

def compare(new_transaction, old_transaction):
    result = {}
    for transaction in new_transaction:
        if transaction in old_transaction:
            if new_transaction[transaction] > old_transaction[transaction]:
                result[transaction] = old_transaction[transaction] - new_transaction[transaction]
        else:
            result[transaction] = 1
    return result