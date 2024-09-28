import os
import sqlite3

class DbManager:

    def __init__(self):
        self.con = sqlite3.connect("jfblocker.db")
        self.cur = self.con.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS FixtureInfo (failCount int);")