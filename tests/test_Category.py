from Category import Category
from db import Database
import pytest
import os

@pytest.fixture
def category():
    os.remove("transactions.db")
    Database().create()
    return Category()

def test_add(category):
    with category as c:
        c.add(category_name="test_category",transaction_type="test_transaction_type")
        c.cursor.execute("select category, transaction_type from categories")
        result = c.cursor.fetchone()
        assert result[0] == "test_category"
        assert result[1] == "test_transaction_type"
        try:
            c.add(category_name="test_category", transaction_type="test_transaction_type")
        except:
            assert True
        else:
            assert False

def test_delete(category):
    with category as c:
        c.cursor.execute("insert into categories (category,transaction_type) values ('test_category','test_transaction_type')")
        c.delete(1)
        c.cursor.execute("select category, transaction_type from categories where delete_date is null")
        result = c.cursor.fetchone()
        assert result is None



def test_get_all(category):
    with category as c:
        c.cursor.execute("insert into categories (category,transaction_type) values ('test_category1','test_transaction_type1')")
        c.cursor.execute("insert into categories (category,transaction_type) values ('test_category2','test_transaction_type1')")
        categories = c.get_all()
        assert categories[0]["category"] == "test_category1"
        assert categories[0]["transaction_type"] == "test_transaction_type1"
        assert categories[1]["category"] == "test_category2"
        assert categories[1]["transaction_type"] == "test_transaction_type1"


def test_get_id(category):
    with category as c:
        c.cursor.execute("insert into categories (category,transaction_type) values ('test_category1','test_transaction_type1')")
        assert c.get_id("test_category1") == 1


def test_get_value_by_id(category):
    with category as c:
        c.cursor.execute("insert into categories (category,transaction_type) values ('test_category1','test_transaction_type1')")
        result = c.get_value_by_id(1)
        assert result[0] == "test_category1"
        assert result[1] == "test_transaction_type1"

