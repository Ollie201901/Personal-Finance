import turtledemo.penrose

import pytest
from datetime import datetime
import utils


@pytest.fixture
def trans0():
    return utils.Tran()


def test_date(trans0):
    trans0.date = "2025-12-02"
    assert isinstance(trans0.date, datetime)
    assert trans0.date == datetime(year=2025, month=12, day=2)
    trans0.date = datetime.today()
    assert isinstance(trans0.date, datetime)
    assert trans0.date == datetime.today()


def test_description(trans0):
    trans0.description = "test"
    assert trans0.description == "test"


def test_amount(trans0):
    assert trans0.amount == 0
    trans0.amount = 1
    assert trans0.amount == 1
    trans0.amount = 0.1
    assert trans0.amount == 0.1
    trans0.amount = -1
    assert trans0.amount == 1


def test_source(trans0):
    trans0.source = "test"
    assert trans0.source == "test"


@pytest.fixture
def trans():
    t = utils.Transactions()
    return t


def test_get_value(trans):
    trans.add(date=datetime.today(), description="desc", amount=10, source="src")
    k = list(trans.keys())[0]
    assert k.date == datetime.today()

def test_add(trans):
    trans.add(date=datetime.today(), description="desc", amount=10, source="src")
    k = list(trans.keys())[0]
    assert k.date == datetime.today()
    assert k.description == "desc"
    assert k.amount == 10
    assert k.source == "src"

@pytest.fixture
def T():
    return utils.Transactions()

def test__lst_of_dict_add(T):
    var = [
        {
            "Date": "2025-03-27",
            "Description": "Test",
            "Sub-description": "Test",
            "Amount": "10.1"
        },
        {
            "Date": "2025-03-27",
            "Description": "Test2",
            "Sub-description": "Test",
            "Amount": "10.1"
        },
        {
            "Date": "2025-03-27",
            "Description": "Test3",
            "Sub-description": "Test",
            "Amount": "10.1"
        },
    ]
    T._lst_of_dict_add(var,"id")
    k = list(T.keys())[0]
    assert k.date == datetime(year=2025,month=3,
                              day=27) and k.description == "Test Test" and k.amount == 10.1 and k.source == "id"
    assert len(T.keys()) == 3
    var = [
        {
            "date": "2025-03-27",
            "description": "Test",
            "sub-description": "Test",
            "amount": "10.1"
        },
        {
            "date": "2025-03-27",
            "description": "Test2",
            "sub-description": "Test",
            "amount": "10.1"
        },
        {
            "date": "2025-03-27",
            "description": "Test3",
            "sub-description": "Test",
            "amount": "10.1"
        },
    ]
    T._lst_of_dict_add(var, "id")
    k = list(T.keys())[0]
    assert k.date == datetime(year=2025, month=3,
                              day=27) and k.description == "Test Test" and k.amount == 10.1 and k.source == "id"
    assert len(T.keys()) == 3
    for i in range(len(var)):
        var[i]["source"] = "test"
    T=utils.Transactions()
    T._lst_of_dict_add(var)
    k = list(T.keys())[0]
    assert k.date == datetime(year=2025, month=3,
                              day=27)
    assert k.description == "Test"
    assert k.amount == 10.1
    assert k.source == "test"
    assert len(T.keys()) == 3

def test_add_csv(T):
    T.add_csv("Basic_1.csv","Chequing")
    k = list(T.keys())[0]
    assert k.date == datetime(year=2025, month=3,day=22)
    assert k.description == "service charge Monthly Fees"
    assert k.amount == 3.95
    assert k.source == "Chequing"
    assert len(T.keys()) == 9
    T.add_csv("Scotia_Momentum_VISA_Infinite_1.csv", "Visa")
    k = list(T.keys())[9]
    assert k.date == datetime(year=2025, month=3, day=27)
    assert k.description == "winners/homesense 248/042"
    assert k.amount == 247.71
    assert k.source == "Visa"
    assert len(T.keys()) == 14+9


def test_get_database():
    assert False


def test_compare():
    assert False


def test_add_to_database():
    assert False


def test_fill_unknown():
    assert False


def test_bulk_import():
    assert False

