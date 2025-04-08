from AutoAssignment import AutoAssignment
from TransactionSource import TransactionSource
from Category import Category
from Vendor import Vendor
from db import Database
import pytest
import os

@pytest.fixture
def auto():
    os.remove("transactions.db")
    Database().create()
    Category().add("TestCategory","TestTransactionType")
    Vendor().add("Starbucks")
    TransactionSource().add("C:","test","visa")
    return AutoAssignment()

def test_add(auto):
    with auto as a:
        a.add(description= "test", min_amount=None, max_amount=None,
              transaction_source = None, category = "TestCategory",
              vendor = "Starbucks")
        a.cursor.execute("select description, min_amount, max_amount, transaction_source_id, category_id, vendor_id from auto_assignment")
        result = a.cursor.fetchone()
        assert result[0] == "test"
        assert result[1] is None
        assert result[2] is None
        assert result[3] is None
        assert result[4] == 1
        assert result[5] == 1
        a.add(description="test", min_amount=0, max_amount=100,
              transaction_source="visa", category="TestCategory",
              vendor="Starbucks")
        a.cursor.execute("select description, min_amount, max_amount, transaction_source_id, category_id, vendor_id from auto_assignment where id = 2")
        result = a.cursor.fetchone()
        assert result[0] == "test"
        assert result[1] == 0
        assert result[2] == 100
        assert result[3] == 1
        assert result[4] == 1
        assert result[5] == 1

def test_delete(auto):
    with auto as a:
        a.cursor.execute("""insert into auto_assignment (description, min_amount, max_amount, transaction_source_id, category_id, vendor_id) 
                                                    values ('test',0,30,1,1,1)""")
        a.delete(1)
        a.cursor.execute("select description, min_amount, max_amount, transaction_source_id, category_id, vendor_id from auto_assignment where delete_date is null")
        result = a.cursor.fetchone()
        assert result is None



def test_get_all(auto):
    with auto as a:
        a.cursor.execute("""insert into auto_assignment (description, min_amount, max_amount, transaction_source_id, category_id, vendor_id) 
                                                    values ('test',0,30,1,1,1)""")
        a.cursor.execute("""insert into auto_assignment (description, min_amount, max_amount, transaction_source_id, category_id, vendor_id) 
                                                    values ('test',0,30,1,1,1)""")
        autos = a.get_all()
        assert autos[0]["description"] == "test"
        assert autos[0]["min_amount"] == 0
        assert autos[0]["max_amount"] == 30
        assert autos[0]["source"] == "visa"
        assert autos[0]["category"] == "TestCategory"
        assert autos[0]["vendor"] == "Starbucks"
        assert autos[1]["description"] == "test"
        assert autos[1]["min_amount"] == 0
        assert autos[1]["max_amount"] == 30
        assert autos[1]["source"] == "visa"
        assert autos[1]["category"] == "TestCategory"
        assert autos[1]["vendor"] == "Starbucks"


