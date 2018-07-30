import psutil
import time
import matplotlib.pyplot as plt
import datetime as dt

start_point = psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_recv / 1024 / 1024
data = []
time_stamps = []
seconds = 0

try:
    while True:
        entry = psutil.net_io_counters(pernic=True)["Wi-Fi"].bytes_recv / 1024 / 1024 - start_point
        seconds += 1
        time_stamps.append(str(dt.datetime.now().hour) + ":" + str(dt.datetime.now().minute) + ":" + str(dt.datetime.now().second))
        data.append(entry)
        print(entry, "MB")
        time.sleep(1)

except KeyboardInterrupt:
    pass

ax1 = plt.subplot2grid( (1, 1), (0, 0) )
ax1.xaxis.set_major_locator(plt.MaxNLocator(5))
ax1.grid(True)
ax1.fill_between(time_stamps, data, alpha = 0.3, color = 'g')

plt.xticks(rotation = -45)
plt.plot(time_stamps, data, color = 'g')

plt.xlabel("Time of the day")
plt.ylabel("Data used (MB)")
plt.title("Data usage")
plt.show()

