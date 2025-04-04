import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("transactions.db")
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

    def create(self):
        try:
            sql = """
                CREATE TABLE IF NOT EXISTS "categories" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "category"  INTEGER NOT NULL,
                    "transaction_type" TEXT NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
            self.cursor.execute(sql)
            sql = """
                CREATE TABLE IF NOT EXISTS "vendors" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "vendor"  INTEGER NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
            self.cursor.execute(sql)
            sql = """
                CREATE TABLE IF NOT EXISTS "budget" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "category_id"  INTEGER NOT NULL,
                    "threshold_per_period"	REAL NOT NULL,
                    "period_days"	INTEGER NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY(category_id) REFERENCES categories(id)
                );
            """
            self.cursor.execute(sql)
            sql = """
                CREATE TABLE IF NOT EXISTS "transactions" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "date"	TEXT NOT NULL,
                    "description"	TEXT NOT NULL,
                    "amount"	REAL NOT NULL,
                    "source"	TEXT NOT NULL,
                    "category_id"	INTEGER NOT NULL,
                    "vendor_id" INTEGER NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT),
                    FOREIGN KEY(category_id) REFERENCES categories(id),
                    FOREIGN KEY(vendor_id) REFERENCES vendors(id)
                );
            """
            self.cursor.execute(sql)
            sql = """
                CREATE TABLE IF NOT EXISTS "transaction_sources" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "folder_path"  TEXT NOT NULL,
                    "file_identifier"	TEXT NOT NULL,
                    "account_alias"	TEXT NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
            self.cursor.execute(sql)
            sql = """
                CREATE TABLE IF NOT EXISTS "auto_assignment" (
                    "id"	INTEGER NOT NULL UNIQUE,
                    "description"  TEXT NOT NULL,
                    "min_amount"	REAL,
                    "max_amount"	REAL,
                    "transaction_source_id" INTEGER,
                    "category_id" INTEGER NOT NULL,
                    "vendor_id" INTEGER NOT NULL,
                    "create_date"	TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    "delete_date"	TEXT,
                    PRIMARY KEY("id" AUTOINCREMENT)
                );
            """
            self.cursor.execute(sql)
        except Exception as e:
            raise e