import sqlite3
from Transaction import Transaction
from datetime import datetime

DB_NAME = "database"

def create_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        query = """
                CREATE TABLE "category" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "category"	TEXT NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                )
                """
        cursor.execute(query)
        query = """
                CREATE TABLE "transaction_type" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "transaction_type"	TEXT NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                )
                """
        cursor.execute(query)
        query = """
                CREATE TABLE "transactions" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "date"	TEXT NOT NULL,
                    "description"	TEXT NOT NULL,
                    "amount"	REAL NOT NULL,
                    "transaction_type_id"	INTEGER NOT NULL,
                    "category_id"	INTEGER,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY("category_id") REFERENCES "category"("id"),
                    FOREIGN KEY("transaction_type_id") REFERENCES "transaction_type"("id")
                )
                """
        cursor.execute(query)
        query = """
                CREATE TABLE "tags" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "tag"	TEXT NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                )
                """
        cursor.execute(query)
        query = """
                CREATE TABLE "transaction_tag" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "transaction_id"	INTEGER NOT NULL,
                    "tag_id"	INTEGER NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                )
                """
        cursor.execute(query)
        cursor.close()
    except: return False
    finally:
        if conn:
            conn.close()
        return True

def bulk_import_from_csv(data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for row in data:
        cursor.execute('''
                        INSERT INTO transactions (date, description, amount)
                        VALUES (?, ?, ?)
                    ''', (row.get('Date'), row.get('Description'), row.get('Amount')))
    conn.commit()
    conn.close()
