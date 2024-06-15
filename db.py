import sqlite3
import logging

from sqlite3 import Error

from model import ToysModel
from queries import CREATE_TABLE, INSERT_TOY, SELECT_ALL_TOYS, SELECT_TOY_BY_ID, UPDATE_TOY_BY_ID


class ToysDb:
    def __init__(self):
        self.conn = sqlite3.connect("toys_db.db")
        self.cur = self.conn.cursor()

    def create_table(self):
        try:
            self.cur.execute(CREATE_TABLE)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def insert_toy(self, toy):
        try:
            self.cur.execute(INSERT_TOY, toy)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def select_all_toys(self):
        try:
            rows: list[ToysModel] = self.cur.execute(SELECT_ALL_TOYS).fetchall()
            return rows
        except Error as e:
            logging.error(e)
            return []

    def select_toy_by_id(self, toy_id):
        try:
            row: ToysModel = self.cur.execute(SELECT_TOY_BY_ID, [toy_id]).fetchone()
            return row
        except Error as e:
            logging.error(e)
            return None

    def update_toy_by_id(self, toy):
        try:
            self.cur.execute(UPDATE_TOY_BY_ID, toy)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def remove_toy_by_id(self, toy_id):
        try:
            self.cur.execute(UPDATE_TOY_BY_ID, toy_id)
            self.conn.commit()
            return True
        except Error as e:
            logging.error(e)
            return False

    def _del__(self):
        if self.conn is not None:
            self.conn.close()


db = ToysDb()
