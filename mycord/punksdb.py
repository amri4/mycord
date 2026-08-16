import os
import requests


class PunksDB:

    def __init__(
        self,
        db_name="mycord_data.db",
        server="http://us.monkey-network.xyz:5002"
    ):

        self.db_name = db_name
        self.server = server.rstrip("/")

        self.key_file = "punksdb.txt"

        if not os.path.exists(
            self.key_file
        ):

            with open(
                self.key_file,
                "w",
                encoding="utf-8"
            ) as file:

                file.write(
                    "PUT_YOUR_PUNKSDB_KEY_HERE"
                )

            raise RuntimeError(
                "punksdb.txt was created. "
                "Put your PunksDB key inside it "
                "and restart the bot."
            )

        with open(
            self.key_file,
            "r",
            encoding="utf-8"
        ) as file:

            self.key = file.read().strip()

        if not self.key:

            raise RuntimeError(
                "punksdb.txt is empty."
            )

    # =========================================
    # REQUEST
    # =========================================

    def _request(
        self,
        action,
        **data
    ):

        response = requests.post(
            f"{self.server}/request",
            json={
                "action": action,
                "db_name": self.db_name,
                **data
            },
            headers={
                "X-PunksDB-Key": self.key
            },
            timeout=10
        )

        response.raise_for_status()

        result = response.json()

        if not result.get(
            "success"
        ):

            raise RuntimeError(
                result.get(
                    "error",
                    "PunksDB request failed."
                )
            )

        return result.get(
            "result"
        )

    # =========================================
    # CREATE TABLE
    # =========================================

    def create_table(
        self,
        name,
        columns
    ):

        return self._request(
            "create_table",
            table=name,
            columns=columns
        )

    # =========================================
    # ADD COLUMN
    # =========================================

    def add_column(
        self,
        table,
        column,
        column_type
    ):

        return self._request(
            "add_column",
            table=table,
            column=column,
            column_type=column_type
        )

    # =========================================
    # INSERT
    # =========================================

    def insert(
        self,
        table,
        columns,
        values
    ):

        return self._request(
            "insert",
            table=table,
            columns=columns,
            values=list(values)
        )

    # =========================================
    # INSERT OR REPLACE
    # =========================================

    def insert_replace(
        self,
        table,
        columns,
        values
    ):

        return self._request(
            "insert_replace",
            table=table,
            columns=columns,
            values=list(values)
        )

    # =========================================
    # FETCH ONE
    # =========================================

    def fetchone(
        self,
        table,
        condition=None,
        values=()
    ):

        return self._request(
            "fetchone",
            table=table,
            condition=condition,
            values=list(values)
        )

    # =========================================
    # FETCH ALL
    # =========================================

    def fetchall(
        self,
        table
    ):

        return self._request(
            "fetchall",
            table=table
        )

    # =========================================
    # UPDATE
    # =========================================

    def update(
        self,
        table,
        set_values,
        condition,
        values
    ):

        return self._request(
            "update",
            table=table,
            set_values=set_values,
            condition=condition,
            values=list(values)
        )

    # =========================================
    # DELETE
    # =========================================

    def delete(
        self,
        table,
        condition,
        values
    ):

        return self._request(
            "delete",
            table=table,
            condition=condition,
            values=list(values)
        )

    # =========================================
    # EXISTS
    # =========================================

    def exists(
        self,
        table,
        condition,
        values
    ):

        return self._request(
            "exists",
            table=table,
            condition=condition,
            values=list(values)
        )

    # =========================================
    # DROP TABLE
    # =========================================

    def drop_table(
        self,
        name
    ):

        return self._request(
            "drop_table",
            table=name
        )

    # =========================================
    # CLOSE
    # =========================================

    def close(self):

        pass
