from Budget import Budget
from Category import Category
from db import Database
import pytest
import os

@pytest.fixture
def budget():
    os.remove("transactions.db")
    Database().create()
    Category().add("TestCategory","TestTransactionType")
    return Budget()

def test_add(budget):
    with budget as b:
        b.add(category= "TestCategory", threshold_per_period= 0, period_days= 30)
        b.cursor.execute("select category_id, threshold_per_period, period_days from budget")
        result = b.cursor.fetchone()
        assert result[0] == 1
        assert result[1] == 0
        assert result[2] == 30

def test_delete(budget):
    with budget as b:
        b.cursor.execute("insert into budget (category_id, threshold_per_period, period_days) values (1,0,30)")
        b.delete(1)
        b.cursor.execute("select category_id, threshold_per_period, period_days from budget where delete_date is null")
        result = b.cursor.fetchone()
        assert result is None



def test_get_all(budget):
    with budget as b:
        b.cursor.execute("insert into budget (category_id, threshold_per_period, period_days) values (1,0,30)")
        b.cursor.execute("insert into budget (category_id, threshold_per_period, period_days) values (1,10,3)")
        budgets = b.get_all()
        assert budgets[0]["category"] == "TestCategory"
        assert budgets[0]["threshold_per_period"] == 0
        assert budgets[0]["period_days"] == 30
        assert budgets[1]["category"] == "TestCategory"
        assert budgets[1]["threshold_per_period"] == 10
        assert budgets[1]["period_days"] == 3


