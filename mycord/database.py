import sqlite3

class DB:
    def __init__(self, db_name="mycord_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, name: str, columns: str):
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} ({columns})")
        self.conn.commit()

    def insert(self, table: str, columns: str, values: tuple):
        placeholders = ", ".join(["?"] * len(values))
        self.cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
        self.conn.commit()

    def insert_replace(self, table: str, columns: str, values: tuple):
        placeholders = ", ".join(["?"] * len(values))
        self.cursor.execute(f"INSERT OR REPLACE INTO {table} ({columns}) VALUES ({placeholders})", values)
        self.conn.commit()

    def fetchone(self, table: str, condition: str = None, values: tuple = ()):
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        self.cursor.execute(query, values)
        return self.cursor.fetchone()

    def fetchall(self, table: str):
        self.cursor.execute(f"SELECT * FROM {table}")
        return self.fetchall()

    def update(self, table: str, set_values: str, condition: str, values: tuple):
        self.cursor.execute(f"UPDATE {table} SET {set_values} WHERE {condition}", values)
        self.conn.commit()

    def delete(self, table: str, condition: str, values: tuple):
        self.cursor.execute(f"DELETE FROM {table} WHERE {condition}", values)
        self.conn.commit()

    def exists(self, table: str, condition: str, values: tuple) -> bool:
        self.cursor.execute(f"SELECT 1 FROM {table} WHERE {condition} LIMIT 1", values)
        return self.cursor.fetchone() is not None

    def close(self):
        self.conn.close()

