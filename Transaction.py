from db import Database
from datetime import datetime
from Category import Category
from Vendor import Vendor

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
                        category, transaction_type = c.get_value_by_id(id=row[5])
                    r["category"] = category
                    r["transaction_type"] = transaction_type
                    with Vendor() as v:
                        vendor = v.get_value_by_id(id=row[6])
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