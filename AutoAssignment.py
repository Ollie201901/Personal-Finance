from db import Database
from datetime import datetime
from TransactionSource import TransactionSource
from Category import Category
from Vendor import Vendor

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
                        transaction_source = t.get_value_by_id(row[4])
                    r["source"] = transaction_source
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