from db import Database
from datetime import datetime

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
    def get_value_by_id(self, id):
        try:
            sql = """
                        SELECT folder_path, file_identifier, account_alias
                        FROM transaction_sources
                        WHERE delete_date is null and id = ?
                    """
            self.cursor.execute(sql, (id,))
            result = self.cursor.fetchone()
            return result
        except Exception as e:
            self.conn.close()
            raise e