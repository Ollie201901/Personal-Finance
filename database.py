import sqlite3
from datetime import datetime

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

class Category(Database):
    def __init__(self):
        super().__init__()

    def add(self,category_name,transaction_type):
        try:
            if self.is_unique(category_name):
                sql = """
                    INSERT INTO categories (category, transaction_type)
                    VALUES(?,?)
                """
                self.cursor.execute(sql, (category_name,transaction_type))
            else: raise Exception("Category already exists")
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()

    def delete(self, id):
        try:
            sql = """
                UPDATE categories
                SET delete_date = ?
                WHERE id = ?;
            """
            self.cursor.execute(sql,(datetime.now(), id))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()

    def get_all(self):
        try:
            sql = """
                SELECT id, category, transaction_type
                FROM categories
                WHERE delete_date is null
            """
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                r = {}
                r["id"] = row[0]
                r["category"] = row[1]
                r["transaction_type"] = row[2]
                result.append(r)
            return result
        except Exception as e:
            self.conn.close()
            raise e

    def get_id(self,category_name):
        try:
            sql = """
                SELECT id
                FROM categories
                WHERE delete_date is null and category = ?
            """
            self.cursor.execute(sql,(category_name,))
            result = self.cursor.fetchone()
            return result[0]
        except Exception as e:
            self.conn.close()
            raise e
    def get_category_by_id(self,id):
        try:
            sql = """
                        SELECT category, transaction_type
                        FROM categories
                        WHERE delete_date is null and id = ?
                    """
            self.cursor.execute(sql, (id,))
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            self.conn.close()
            raise e

    def is_unique(self, category_name):
        try:
            sql = """
                        SELECT category
                        FROM categories
                        WHERE delete_date is null and category = ?
                    """
            self.cursor.execute(sql, (category_name,))
            result = self.cursor.fetchone()
            return result is None
        except Exception as e:
            self.conn.close()
            raise e

class Vendor(Database):
    def __init__(self):
        super().__init__()

    def add(self,vendor_name):
        try:
            if self.is_unique(vendor_name):
                sql = """
                    INSERT INTO vendors (vendor)
                    VALUES(?)
                """
                self.cursor.execute(sql, (vendor_name,))
            else:
                raise Exception("Vendor already exists")
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()

    def delete(self, id):
        try:
            sql = """
                UPDATE vendors
                SET delete_date = ?
                WHERE id = ?;
            """
            self.cursor.execute(sql,(datetime.now(), id))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()

    def get_all(self):
        try:
            sql = """
                SELECT id, vendor
                FROM vendors
                WHERE delete_date is null
            """
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                r = {}
                r["id"] = row[0]
                r["vendor"] = row[1]
                result.append(r)
            return result
        except Exception as e:
            self.conn.close()
            raise e

    def get_id(self,vendor_name):
        try:
            sql = """
                SELECT id
                FROM vendors
                WHERE delete_date is null and vendor = ?
            """
            self.cursor.execute(sql,(vendor_name,))
            result = self.cursor.fetchone()
            return result[0]
        except Exception as e:
            self.conn.close()
            raise e
    def get_category_by_id(self,id):
        try:
            sql = """
                        SELECT vendor
                        FROM vendors
                        WHERE delete_date is null and id = ?
                    """
            self.cursor.execute(sql, (id,))
            result = self.cursor.fetchone()
            return result[0]
        except Exception as e:
            self.conn.close()
            raise e

    def is_unique(self, vendor_name):
        try:
            sql = """
                        SELECT vendor
                        FROM vendors
                        WHERE delete_date is null and vendor = ?
                    """
            self.cursor.execute(sql, (vendor_name,))
            result = self.cursor.fetchone()
            return result is None
        except Exception as e:
            self.conn.close()
            raise e

class Budget(Database):
    def __init__(self):
        super().__init__()

    def add(self,category, threshold_per_period, period_days):
        try:
            sql = """
                INSERT INTO budget (category_id, threshold_per_period, period_days)
                VALUES(?,?,?)
            """
            category_id = Category().get_id(category)
            self.cursor.execute(sql, (category_id, threshold_per_period, period_days))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()
    def get_all(self):
        try:
            sql = """
                SELECT id, category_id, threshold_per_period, period_days
                FROM budget
                WHERE delete_date is null
            """
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                r = {}
                r["id"] = row[0]
                with Category() as c:
                    category, transaction_type = c.get_category_by_id(id=row[1])
                r["category"] = category
                r["transaction_type"] = transaction_type
                r["threshold_per_period"] = row[2]
                r["period_days"] = row[3]
                result.append(r)
            return result
        except Exception as e:
            self.conn.close()
            raise e

    def delete(self, id):
        try:
            sql = """
                UPDATE budget
                SET delete_date = ?
                WHERE id = ?;
            """
            self.cursor.execute(sql,(datetime.now(), id))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()
class TransactionSource(Database):
    def __init__(self):
        super().__init__()

    def add(self, folder_path, file_identifier, account_alias):
        try:
            sql = """
                INSERT INTO transaction_sources (folder_path, file_identifier, account_alias)
                VALUES(?,?,?)
            """
            self.cursor.execute(sql, (folder_path, file_identifier, account_alias))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()
    def delete(self,id):
        try:
            sql = """
                UPDATE transaction_sources
                SET delete_date = ?
                WHERE id = ?;
            """
            self.cursor.execute(sql,(datetime.now(), id))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()

    def get_all(self):
        try:
            sql = """
                SELECT id, folder_path, file_identifier, account_alias
                FROM transaction_sources
                WHERE delete_date is null
            """
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            result = []
            for row in rows:
                r = {}
                r["id"] = row[0]
                r["folder_path"] = row[1]
                r["file_identifier"] = row[2]
                r["account_alias"] = row[3]
                result.append(r)
            return result
        except Exception as e:
            self.conn.close()
            raise e

    def get_id(self,source_name):
        try:
            sql = """
                SELECT id
                FROM transaction_sources
                WHERE delete_date is null and account_alias = ?
            """
            self.cursor.execute(sql,(source_name,))
            result = self.cursor.fetchone()
            return result[0]
        except Exception as e:
            self.conn.close()
            raise e
    def get_category_by_id(self,id):
        try:
            sql = """
                        SELECT vendor
                        FROM vendors
                        WHERE delete_date is null and id = ?
                    """
            self.cursor.execute(sql, (id,))
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            self.conn.close()
            raise e

class Transaction(Database):
    def __init__(self):
        super().__init__()

    def add(self, date, description, amount, source, category=None, vendor = None):
        try:
            sql = """
                INSERT INTO transactions (date, description, amount, source, category_id, vendor_id)
                VALUES(?, ?, ?, ?, ?, ?)
            """
            with Category() as c:
                category_id = c.get_id(category)
            with Vendor() as v:
                vendor_id = v.get_id(vendor)
            self.cursor.execute(sql, (date, description, amount, source, category_id,vendor_id))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()
    def get_all(self):
            try:
                sql = """
                    SELECT id, date, description, amount, source, category_id, vendor_id
                    FROM transactions
                    WHERE delete_date is null
                """
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                result = []
                for row in rows:
                    r = {}
                    r["id"] = row[0]
                    r["date"] = row[1]
                    r["description"] = row[2]
                    r["amount"] = row[3]
                    r["source"] = row[4]
                    with Category() as c:
                        category, transaction_type = c.get_category_by_id(id=row[5])
                    r["category"] = category
                    r["transaction_type"] = transaction_type
                    with Vendor() as v:
                        vendor = v.get_category_by_id(id=row[6])
                    r["vendor"] = vendor
                    result.append(r)
                return result
            except Exception as e:
                self.conn.close()
                raise e

    def delete(self, id):
        try:
            sql = """
                UPDATE transactions
                SET delete_date = ?
                WHERE id = ?;
            """
            self.cursor.execute(sql,(datetime.now(), id))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()

class AutoAssignment(Database):
    def __init__(self):
        super().__init__()

    def add(self, description, min_amount, max_amount, transaction_source = None, category = None, vendor = None):
        try:
            sql = """
                INSERT INTO auto_assignment (description, min_amount, max_amount, transaction_source_id, category_id, vendor_id)
                VALUES(?, ?, ?, ?, ?, ?)
            """
            with TransactionSource() as t:
                transaction_source_id = t.get_id(transaction_source)
            with Category() as c:
                category_id = c.get_id(category)
            with Vendor() as v:
                vendor_id = v.get_id(vendor)
            self.cursor.execute(sql, (description, min_amount, max_amount, transaction_source_id, category_id, vendor_id))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()
    def get_all(self):
            try:
                sql = """
                    SELECT id, description, min_amount, max_amount, transaction_source_id, category_id, vendor_id
                    FROM auto_assignment
                    WHERE delete_date is null
                """
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                result = []
                for row in rows:
                    r = {}
                    r["id"] = row[0]
                    r["description"] = row[1]
                    r["min_amount"] = row[2]
                    r["max_amount"] = row[3]
                    with TransactionSource() as t:
                        transaction_source = t.get_category_by_id(row[4])
                    r["source"] = transaction_source
                    with Category() as c:
                        category, transaction_type = c.get_category_by_id(id=row[5])
                    r["category"] = category
                    r["transaction_type"] = transaction_type
                    with Vendor() as v:
                        vendor = v.get_category_by_id(id=row[6])
                    r["vendor"] = vendor
                    result.append(r)
                return result
            except Exception as e:
                self.conn.close()
                raise e

    def delete(self,id):
        try:
            sql = """
                UPDATE auto_assignment
                SET delete_date = ?
                WHERE id = ?;
            """
            self.cursor.execute(sql,(datetime.now(), id))
        except Exception as e:
            self.conn.rollback()
            self.conn.close()
            raise e
        else:
            self.conn.commit()
            self.conn.close()