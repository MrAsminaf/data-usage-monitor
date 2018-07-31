import sqlite3
import datetime as dt

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()

        self.date = dt.datetime.today().strftime('%d-%m-%Y')
        self.cursor.execute("CREATE TABLE IF NOT EXISTS '"+str(self.date)+"' (hour TEXT, download REAL, upload REAL)")
        self.cursor.execute("DELETE FROM '"+str(self.date)+"'")

    def PushData(self, time, download, upload):
        self.cursor.execute("INSERT INTO '{}' values('{}', {}, {})".format(self.date, time, download, upload))
        self.connection.commit()
