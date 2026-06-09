import sqlite3

# =========================================
# CONNECT
# =========================================

# Keeps your exact global setup
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# =========================================
# HELPER TO SWITCH DATABASE FILE DYNAMICALLY
# =========================================

def _switch_db(db_name):
    """Closes the current connection and opens a new one named after the table."""
    global conn, cursor
    conn.close()
    conn = sqlite3.connect(f"{db_name}.db")
    cursor = conn.cursor()

# =========================================
# CREATE TABLE
# =========================================

def create_table(name, columns):

    _switch_db(name)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {name} (
        {columns}
    )
    """)

    conn.commit()

# =========================================
# INSERT
# =========================================

def insert(table, columns, values):

    _switch_db(table)

    placeholders = ", ".join(
        ["?"] * len(values)
    )

    cursor.execute(f"""
    INSERT INTO {table}
    ({columns})

    VALUES ({placeholders})
    """, values)

    conn.commit()

# =========================================
# INSERT OR REPLACE
# =========================================

def insert_replace(table, columns, values):

    _switch_db(table)

    placeholders = ", ".join(
        ["?"] * len(values)
    )

    cursor.execute(f"""
    INSERT OR REPLACE INTO {table}
    ({columns})

    VALUES ({placeholders})
    """, values)

    conn.commit()

# =========================================
# SELECT ONE
# =========================================

def fetchone(table, condition=None, values=()):

    _switch_db(table)

    query = f"SELECT * FROM {table}"

    if condition:
        query += f" WHERE {condition}"

    cursor.execute(query, values)

    return cursor.fetchone()

# =========================================
# SELECT ALL
# =========================================

def fetchall(table):

    _switch_db(table)

    cursor.execute(f"""
    SELECT * FROM {table}
    """)

    return cursor.fetchall()

# =========================================
# UPDATE
# =========================================

def update(table, set_values, condition, values):

    _switch_db(table)

    cursor.execute(f"""
    UPDATE {table}
    SET {set_values}
    WHERE {condition}
    """, values)

    conn.commit()

# =========================================
# DELETE
# =========================================

def delete(table, condition, values):

    _switch_db(table)

    cursor.execute(f"""
    DELETE FROM {table}
    WHERE {condition}
    """, values)

    conn.commit()

# =========================================
# EXISTS
# =========================================

def exists(table, condition, values):

    _switch_db(table)

    cursor.execute(f"""
    SELECT * FROM {table}
    WHERE {condition}
    """, values)

    return cursor.fetchone() is not None

# =========================================
# CLOSE
# =========================================

def close():

    conn.close()
