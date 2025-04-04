from db import Database
from datetime import datetime
from Category import Category

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
                    category, transaction_type = c.get_value_by_id(id=row[1])
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