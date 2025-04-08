from TransactionSource import TransactionSource
from db import Database
import pytest
import os

@pytest.fixture
def source():
    os.remove("transactions.db")
    Database().create()
    return TransactionSource()

def test_add(source):
    with source as s:
        s.add(folder_path="C:",file_identifier="test",account_alias="visa")
        s.cursor.execute("select folder_path, file_identifier, account_alias from transaction_sources")
        result = s.cursor.fetchone()
        assert result[0] == "C:"
        assert result[1] == "test"
        assert result[2] == "visa"

def test_delete(source):
    with source as s:
        s.cursor.execute("insert into transaction_sources (folder_path,file_identifier,account_alias)  values ('C:', 'test', 'visa')")
        s.delete(1)
        s.cursor.execute("select folder_path, file_identifier, account_alias from transaction_sources where delete_date is null")
        result = s.cursor.fetchone()
        assert result is None



def test_get_all(source):
    with source as s:
        s.cursor.execute("insert into transaction_sources (folder_path,file_identifier,account_alias)  values ('C:', 'test', 'visa')")
        s.cursor.execute("insert into transaction_sources (folder_path,file_identifier,account_alias)  values ('C://', 'test1', 'visa1')")
        sources = s.get_all()
        assert sources[0]["folder_path"] == "C:"
        assert sources[0]["file_identifier"] == "test"
        assert sources[0]["account_alias"] == "visa"
        assert sources[1]["folder_path"] == "C://"
        assert sources[1]["file_identifier"] == "test1"
        assert sources[1]["account_alias"] == "visa1"

def test_get_id(source):
    with source as s:
        s.cursor.execute("insert into transaction_sources (folder_path,file_identifier,account_alias)  values ('C:', 'test', 'visa')")
        assert s.get_id("visa") == 1


def test_get_value_by_id(source):
    with source as s:
        s.cursor.execute("insert into transaction_sources (folder_path,file_identifier,account_alias)  values ('C:', 'test', 'visa')")
        result = s.get_value_by_id(1)
        assert result[0] == "C:"
        assert result[1] == "test"
        assert result[2] == "visa"