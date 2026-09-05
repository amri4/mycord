import os
import sqlite3


class DB:

    def __init__(
        self,
        db_name="mycord_data.db"
    ):
        # 📂 Ensure the 'data' directory exists locally
        folder_name = "data"

        if not os.path.exists(folder_name):
            os.makedirs(
                folder_name,
                exist_ok=True
            )

        # 🔄 Force the database file path inside
        # the 'data' folder
        self.db_name = os.path.join(
            folder_name,
            db_name
        )

        self.conn = sqlite3.connect(
            self.db_name
        )

        self.cursor = self.conn.cursor()


    def create_table(
        self,
        name,
        columns
    ):
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {name} (
                {columns}
            )
            """
        )

        self.conn.commit()


    def add_column(
        self,
        table,
        column,
        column_type
    ):
        self.cursor.execute(
            f"""
            ALTER TABLE {table}
            ADD COLUMN {column} {column_type}
            """
        )

        self.conn.commit()


    def insert(
        self,
        table,
        columns,
        values
    ):
        placeholders = ", ".join(
            ["?"] * len(values)
        )

        self.cursor.execute(
            f"""
            INSERT INTO {table}
            ({columns})
            VALUES ({placeholders})
            """,
            values
        )

        self.conn.commit()


    def insert_replace(
        self,
        table,
        columns,
        values
    ):
        placeholders = ", ".join(
            ["?"] * len(values)
        )

        self.cursor.execute(
            f"""
            INSERT OR REPLACE INTO {table}
            ({columns})
            VALUES ({placeholders})
            """,
            values
        )

        self.conn.commit()


    def fetchone(
        self,
        table,
        condition=None,
        values=()
    ):
        query = f"SELECT * FROM {table}"

        if condition:
            query += f" WHERE {condition}"

        self.cursor.execute(
            query,
            values
        )

        return self.cursor.fetchone()


    def fetchall(
        self,
        table
    ):
        self.cursor.execute(
            f"SELECT * FROM {table}"
        )

        return self.cursor.fetchall()


    def update(
        self,
        table,
        set_values,
        condition,
        values
    ):
        self.cursor.execute(
            f"""
            UPDATE {table}
            SET {set_values}
            WHERE {condition}
            """,
            values
        )

        self.conn.commit()


    def delete(
        self,
        table,
        condition,
        values
    ):
        self.cursor.execute(
            f"""
            DELETE FROM {table}
            WHERE {condition}
            """,
            values
        )

        self.conn.commit()


    def exists(
        self,
        table,
        condition,
        values
    ):
        self.cursor.execute(
            f"""
            SELECT 1
            FROM {table}
            WHERE {condition}
            """,
            values
        )

        return self.cursor.fetchone() is not None


    def drop_table(
        self,
        name
    ):
        self.cursor.execute(
            f"DROP TABLE IF EXISTS {name}"
        )

        self.conn.commit()


    def close(self):
        self.conn.close()