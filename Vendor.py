from db import Database
from datetime import datetime
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
    def get_value_by_id(self, id):
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