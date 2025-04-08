from db import Database
from datetime import datetime
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

    def get_value_by_id(self, id):
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