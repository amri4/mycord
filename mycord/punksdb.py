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

        if not os.path.exists(self.key_file):
            with open(
                self.key_file,
                "w",
                encoding="utf-8"
            ) as file:
                file.write("PUT_YOUR_PUNKSDB_KEY_HERE")

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


    def _request(self, action, **data):

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

        if not result.get("success"):
            raise RuntimeError(
                result.get(
                    "error",
                    "PunksDB request failed."
                )
            )

        return result.get("result")


    def create_table(self, name, columns):
        return self._request(
            "create_table",
            table=name,
            columns=columns
        )


    def insert(self, table, columns, values):
        return self._request(
            "insert",
            table=table,
            columns=columns,
            values=list(values)
        )


    def insert_replace(self, table, columns, values):
        return self._request(
            "insert_replace",
            table=table,
            columns=columns,
            values=list(values)
        )


    def fetchone(self, table, condition=None, values=()):
        return self._request(
            "fetchone",
            table=table,
            condition=condition,
            values=list(values)
        )


    def fetchall(self, table):
        return self._request(
            "fetchall",
            table=table
        )


    def update(self, table, set_values, condition, values):
        return self._request(
            "update",
            table=table,
            set_values=set_values,
            condition=condition,
            values=list(values)
        )


    def delete(self, table, condition, values):
        return self._request(
            "delete",
            table=table,
            condition=condition,
            values=list(values)
        )


    def exists(self, table, condition, values):
        return self._request(
            "exists",
            table=table,
            condition=condition,
            values=list(values)
        )


    def drop_table(self, name):
        return self._request(
            "drop_table",
            table=name
        )


    def close(self):
        pass
