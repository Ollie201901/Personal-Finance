from Transaction import Transaction
from Category import Category
from Vendor import Vendor
from db import Database
import pytest
import os
from datetime import datetime

@pytest.fixture
def trans():
    os.remove("transactions.db")
    Database().create()
    Category().add("TestCategory","TestTransactionType")
    Vendor().add("Starbucks")
    return Transaction()

def test_add(trans):
    with trans as t:
        t.add(date=datetime(2020,2,1), description = "test", amount = 10, source = "visa", category="TestCategory", vendor = "Starbucks")
        t.cursor.execute("select date, description, amount, source, category_id, vendor_id from transactions")
        result = t.cursor.fetchone()
        assert datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S').date() == datetime(2020,2,1).date()
        assert result[1] == "test"
        assert result[2] == 10
        assert result[3] == "visa"
        assert result[4] == 1
        assert result[5] == 1

def test_delete(trans):
    with trans as t:
        t.cursor.execute("insert into transactions (date, description, amount, source, category_id, vendor_id) values (?,?,?,?,?,?)",
                         (datetime(2020,2,1),"test",10,'visa',1,1))
        t.delete(1)
        t.cursor.execute("select date, description, amount, source, category_id, vendor_id from transactions where delete_date is null")
        result = t.cursor.fetchone()
        assert result is None



def test_get_all(trans):
    with trans as t:
        t.cursor.execute("insert into transactions (date, description, amount, source, category_id, vendor_id) values (?,?,?,?,?,?)",
                         (datetime(2020,2,1),"test",10,'visa',1,1))
        t.cursor.execute("insert into transactions (date, description, amount, source, category_id, vendor_id) values (?,?,?,?,?,?)",
                         (datetime(2020, 2, 2), "test1", 20, 'visa1', 1, 1))
        transactions = t.get_all()
        assert transactions[0]["date"] == datetime(2020,2,1).date()
        assert transactions[0]["description"] == "test"
        assert transactions[0]["amount"] == 10
        assert transactions[0]["source"] == "visa"
        assert transactions[0]["category"] == "TestCategory"
        assert transactions[0]["vendor"] == "Starbucks"
        assert transactions[1]["date"] == datetime(2020, 2, 2).date()
        assert transactions[1]["description"] == "test1"
        assert transactions[1]["amount"] == 20
        assert transactions[1]["source"] == "visa1"
        assert transactions[1]["category"] == "TestCategory"
        assert transactions[1]["vendor"] == "Starbucks"


