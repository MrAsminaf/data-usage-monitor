import psutil
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import datetime as dt
from db_manager import *
import pickle
import os.path

def CalculateDownload():
    return psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_recv / 1024 / 1024 - download_start_point

def CalculateUpload():
    return psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_sent / 1024 / 1024 - upload_start_point

def animate(i):
    # Get current upload and download
    up = CalculateUpload()
    down = CalculateDownload()

    # Calculate data for y axis
    entry = up + down

    # Get current time for x axis
    current_time = str(dt.datetime.now().hour) + ":" + str(dt.datetime.now().minute) + ":" + str(dt.datetime.now().second)

    # Add data to the x and y axis
    time_stamps.append(current_time)
    data.append(entry)

    # Set properties of the plot
    ax1.clear()
    ax1.fill_between(time_stamps, data, alpha = 0.3, color = 'g')
    plt.xlabel("Time of the day")
    plt.ylabel("Data used (MB)")
    plt.title("Data usage")
    plt.xticks(rotation = -45)
    ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
    ax1.grid(True)
    ax1.plot(time_stamps, data, color = 'g')

    # Insert data to database
    db.PushData(current_time, down, up)


if __name__ == "__main__":
    # Container for y and x axis
    data = []
    time_stamps = []

    db = Database(data, time_stamps)
    fig = plt.figure()
    ax1 = plt.subplot(1, 1, 1)
    filename = "startpoints-"+dt.datetime.today().strftime('%d-%m-%Y')

    # If startpoints file doesn't exist
    if not os.path.isfile(filename):
        # Calculate starting points for downloaded updated data
        download_start_point = psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_recv / 1024 / 1024
        upload_start_point = psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_sent / 1024 / 1024
        pickle.dump([download_start_point, upload_start_point], open(filename, "wb"))
    else:
        # Else read the data from the file
        download_start_point = pickle.load(open(filename, "rb"))[0]
        upload_start_point = pickle.load(open(filename, "rb"))[1]
        db.ReadData(data, time_stamps)

    # Animate the plot every second
    try:
        ani = animation.FuncAnimation(fig, animate, interval = 1000)
        plt.show()
    except KeyboardInterrupt:
        print("Program stopped")
