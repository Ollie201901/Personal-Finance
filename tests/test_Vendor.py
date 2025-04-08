from Vendor import Vendor
from db import Database
import pytest
import os

@pytest.fixture
def vendor():
    os.remove("transactions.db")
    Database().create()
    return Vendor()

def test_add(vendor):
    with vendor as v:
        v.add("Starbucks")
        v.cursor.execute("select vendor from vendors")
        result = v.cursor.fetchone()
        assert result[0] == "Starbucks"
        try:
            v.add("Starbucks")
        except:
            assert True
        else:
            assert False

def test_delete(vendor):
    with vendor as v:
        v.cursor.execute("insert into vendors (vendor) values ('Starbucks')")
        v.delete(1)
        v.cursor.execute("select vendor from vendors where delete_date is null")
        result = v.cursor.fetchone()
        assert result is None



def test_get_all(vendor):
    with vendor as v:
        v.cursor.execute("insert into vendors (vendor) values ('Starbucks')")
        v.cursor.execute("insert into vendors (vendor) values ('Tim Hortons')")
        vendors = v.get_all()
        assert vendors[0]["vendor"] == "Starbucks"
        assert vendors[1]["vendor"] == "Tim Hortons"


def test_get_id(vendor):
    with vendor as v:
        v.cursor.execute("insert into vendors (vendor) values ('Starbucks')")
        assert v.get_id("Starbucks") == 1


def test_get_value_by_id(vendor):
    with vendor as v:
        v.cursor.execute("insert into vendors (vendor) values ('Starbucks')")
        result = v.get_value_by_id(1)
        assert result == "Starbucks"

