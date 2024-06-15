CREATE_TABLE = """CREATE TABLE IF NOT EXISTS toys_tbl (
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    price REAL NOT NULL,
                    seller TEXT NOT NULL,
                    created TEXT NOT NULL,
                    updated DATETIME NOT NULL
                )"""

INSERT_TOY = """
     INSERT INTO toys_tbl (name, description, price, seller, created, updated) VALUES (?, ?, ?, ?, ?, ?)
 """

SELECT_ALL_TOYS = """SELECT * FROM toys_tbl"""

SELECT_TOY_BY_ID = """SELECT * FROM toys_tbl WHERE id = ?"""

UPDATE_TOY_BY_ID = """
UPDATE toys_tbl set name = ?, description = ?, price = ?, seller = ?, created = ?, updated = ? WHERE id = ?"""

REMOVE_TOY_BY_ID = """DELETE FROM toys_tbl WHERE id = ?"""
