import sqlite3
from datetime import datetime, timedelta
from dateutil import rrule

class Database:
    def __init__(self, data, time_stamps):
        self.connection = sqlite3.connect('example.db')
        self.cursor = self.connection.cursor()
        self.date = datetime.today().strftime('%d-%m-%Y')
        self.cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='"+self.date+"';")
        isEmpty = self.cursor.fetchone()
        if(isEmpty[0] == 0):
            self.cursor.execute("CREATE TABLE IF NOT EXISTS '"+str(self.date)+"' (hour TEXT, download REAL, upload REAL)")
        else:
            # Get time difference in seconds between now and the last record
            diff = self.GetTimeDifference()

            # Select last record
            self.cursor.execute("SELECT * FROM '"+self.date+"'ORDER BY download DESC LIMIT 1")

            # Get time of the last record and split between hours, minutes and seconds
            prev_time = self.cursor.fetchone()[0]
            prev_time = prev_time.split(':')

            # Get upload and download data from the last record
            self.cursor.execute("SELECT * FROM '"+self.date+"'ORDER BY download DESC LIMIT 1")
            prev_download = self.cursor.fetchone()[1]
            self.cursor.execute("SELECT * FROM '"+self.date+"'ORDER BY download DESC LIMIT 1")
            prev_upload = self.cursor.fetchone()[2]

            # Make values for datetime object
            ext_prev_time = [datetime.now().year, datetime.now().month, datetime.now().day, prev_time[0], prev_time[1], prev_time[2]]

            # Create datetime object
            date = datetime(*map(int, ext_prev_time))
            later = date + timedelta(seconds = diff)

            for dt in rrule.rrule(rrule.SECONDLY, dtstart=date, until=later):
                self.PushData(str(dt.hour)+':'+str(dt.minute)+':'+str(dt.second), prev_download, prev_upload)

    def PushData(self, time, download, upload):
        self.cursor.execute("INSERT INTO '{}' values('{}', {}, {})".format(self.date, time, download, upload))
        self.connection.commit()

    def ReadData(self, data, time_stamps):
        self.cursor.execute("SELECT * FROM '"+self.date+"'")
        rows = self.cursor.fetchall()
        for row in rows:
            time_stamps.append(row[0])
            data.append(row[1] + row[2])

    def GetTimeDifference(self):
        self.cursor.execute("SELECT * FROM '"+self.date+"'ORDER BY download DESC LIMIT 1")
        prev_time = self.cursor.fetchone()[0]
        print(prev_time)
        seconds = str(prev_time).split(':')
        seconds[0] = int(seconds[0]) * 60 * 60
        seconds[1] = int(seconds[1]) * 60
        total = seconds[0] + int(seconds[1]) + int(seconds[2])

        current = []
        current.append(datetime.now().hour * 60 * 60)
        current.append(datetime.now().minute * 60)
        current.append(datetime.now().second)
        total_curr = current[0] + current[1] + current[2]

        return total_curr - total


