import os
import sqlite3


class DB:

    def __init__(self):
        # 📂 Ensure the 'data' directory exists locally
        self.folder_name = "data"

        os.makedirs(
            self.folder_name,
            exist_ok=True
        )


    def _get_connection(
        self,
        table
    ):
        db_path = os.path.join(
            self.folder_name,
            f"{table}.db"
        )

        return sqlite3.connect(
            db_path
        )


    def create_table(
        self,
        name,
        columns
    ):
        conn = self._get_connection(name)
        cursor = conn.cursor()

        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {name} (
                {columns}
            )
            """
        )

        conn.commit()
        conn.close()


    def add_column(
        self,
        table,
        column,
        column_type
    ):
        conn = self._get_connection(table)
        cursor = conn.cursor()

        cursor.execute(
            f"""
            ALTER TABLE {table}
            ADD COLUMN {column} {column_type}
            """
        )

        conn.commit()
        conn.close()


    def insert(
        self,
        table,
        columns,
        values
    ):
        conn = self._get_connection(table)
        cursor = conn.cursor()

        placeholders = ", ".join(
            ["?"] * len(values)
        )

        cursor.execute(
            f"""
            INSERT INTO {table}
            ({columns})
            VALUES ({placeholders})
            """,
            values
        )

        conn.commit()
        conn.close()


    def insert_replace(
        self,
        table,
        columns,
        values
    ):
        conn = self._get_connection(table)
        cursor = conn.cursor()

        placeholders = ", ".join(
            ["?"] * len(values)
        )

        cursor.execute(
            f"""
            INSERT OR REPLACE INTO {table}
            ({columns})
            VALUES ({placeholders})
            """,
            values
        )

        conn.commit()
        conn.close()


    def fetchone(
        self,
        table,
        condition=None,
        values=()
    ):
        conn = self._get_connection(table)
        cursor = conn.cursor()

        query = f"SELECT * FROM {table}"

        if condition:
            query += f" WHERE {condition}"

        cursor.execute(
            query,
            values
        )

        result = cursor.fetchone()

        conn.close()

        return result


    def fetchall(
        self,
        table
    ):
        conn = self._get_connection(table)
        cursor = conn.cursor()

        cursor.execute(
            f"SELECT * FROM {table}"
        )

        result = cursor.fetchall()

        conn.close()

        return result


    def update(
        self,
        table,
        set_values,
        condition,
        values
    ):
        conn = self._get_connection(table)
        cursor = conn.cursor()

        cursor.execute(
            f"""
            UPDATE {table}
            SET {set_values}
            WHERE {condition}
            """,
            values
        )

        conn.commit()
        conn.close()


    def delete(
        self,
        table,
        condition,
        values
    ):
        conn = self._get_connection(table)
        cursor = conn.cursor()

        cursor.execute(
            f"""
            DELETE FROM {table}
            WHERE {condition}
            """,
            values
        )

        conn.commit()
        conn.close()


    def exists(
        self,
        table,
        condition,
        values
    ):
        conn = self._get_connection(table)
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT 1
            FROM {table}
            WHERE {condition}
            """,
            values
        )

        result = cursor.fetchone() is not None

        conn.close()

        return result


    def drop_table(
        self,
        name
    ):
        db_path = os.path.join(
            self.folder_name,
            f"{name}.db"
        )

        if os.path.exists(db_path):
            os.remove(db_path)