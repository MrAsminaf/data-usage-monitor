import psutil
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
from db_manager import *

def CalculateDownload():
    return psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_recv / 1024 / 1024 - download_start_point

def CalculateUpload():
    return psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_sent / 1024 / 1024 - upload_start_point

#def CalculateUsage():
#    download = psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_recv / 1024 / 1024 - download_start_point
#    upload = psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_recv / 1024 / 1024 - upload_start_point
#    return download + upload

def animate(i):
    try:
        up = CalculateUpload()
        down = CalculateDownload()
        entry = up + down
        current_time = str(dt.datetime.now().hour) + ":" + str(dt.datetime.now().minute) + ":" + str(dt.datetime.now().second)

        time_stamps.append(current_time)
        data.append(entry)

        ax1.clear()
        ax1.fill_between(time_stamps, data, alpha = 0.3, color = 'g')
        plt.xlabel("Time of the day")
        plt.ylabel("Data used (MB)")
        plt.title("Data usage")
        plt.xticks(rotation = -45)
        ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
        ax1.grid(True)
        ax1.plot(time_stamps, data, color = 'g')

        db.PushData(current_time, down, up)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    db = Database()
    download_start_point = psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_recv / 1024 / 1024
    upload_start_point = psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_sent / 1024 / 1024
    data = []
    time_stamps = []

    fig = plt.figure()
    ax1 = plt.subplot(1, 1, 1)

    ani = animation.FuncAnimation(fig, animate, interval = 1000)
    plt.show()

