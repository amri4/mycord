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

        # =========================================
        # CREATE KEY FILE
        # =========================================

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

        # =========================================
        # READ KEY
        # =========================================

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

        if self.key == (
            "PUT_YOUR_PUNKSDB_KEY_HERE"
        ):

            raise RuntimeError(
                "Replace the placeholder in "
                "punksdb.txt with your PunksDB key."
            )

    # =========================================
    # REQUEST
    # =========================================

    def _request(
        self,
        action,
        **data
    ):

        try:

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

        except requests.RequestException as error:

            raise RuntimeError(
                "Could not connect to PunksDB: "
                f"{type(error).__name__}: {error}"
            ) from error

        # =========================================
        # HTTP ERROR
        # =========================================

        if response.status_code != 200:

            # Try JSON first
            try:

                error_data = response.json()

            except ValueError:

                error_data = response.text

            # Convert response into readable text
            if isinstance(
                error_data,
                dict
            ):

                server_error = (
                    error_data.get("error")
                    or error_data.get("message")
                    or str(error_data)
                )

            else:

                server_error = str(
                    error_data
                )

            if not server_error.strip():

                server_error = (
                    "The PunksDB server returned "
                    "an empty error response."
                )

            raise RuntimeError(
                f"PunksDB HTTP "
                f"{response.status_code}: "
                f"{server_error}"
            )

        # =========================================
        # PARSE RESPONSE
        # =========================================

        try:

            result = response.json()

        except ValueError as error:

            raise RuntimeError(
                "PunksDB returned invalid JSON: "
                f"{response.text[:1000]}"
            ) from error

        # =========================================
        # SERVER REPORTED FAILURE
        # =========================================

        if not result.get(
            "success",
            False
        ):

            raise RuntimeError(
                result.get(
                    "error",
                    result.get(
                        "message",
                        "PunksDB request failed."
                    )
                )
            )

        # =========================================
        # RETURN RESULT
        # =========================================

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
