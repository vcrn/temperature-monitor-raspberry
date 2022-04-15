"""
A simple temperature monitor GUI written in Python and tkinter for Raspberry Pi running OS Raspbian. Due to the 
small amount of code, the whole code is placed in one file for ease of transfer even though it might be at the 
cost of a clearer structure.

Author: Victor Nilsson, Date: 2020-10-10, github: vcrn.
"""

import tkinter as tk
import subprocess
from threading import Timer
import signal
import os


def temp_monitor() -> None:
    """
    Changes layout of GUI-window: Adds a divider, labels for CPU and GPU temperature, and changes function and text
    of the button.
    """

    if len(entry_update_interval.get()) > 0:
        update_interval = float(entry_update_interval.get())  # How often to update temperature.
    else:
        update_interval = 5

    label_divider = tk.Label(root, text='________________________________________')
    label_divider.config(font=('helvetica', 10))
    canvas.create_window(160, 100, window=label_divider)

    label_gpu_temp = tk.Label(root, text="GPU temperature: ")
    label_gpu_temp.config(font=('helvetica', 10))
    canvas.create_window(160, 120, window=label_gpu_temp)

    label_cpu_temp = tk.Label(root, text="CPU temperature: ")
    label_cpu_temp.config(font=('helvetica', 10))
    canvas.create_window(160, 140, window=label_cpu_temp)

    button.configure(text='CLOSE MONITOR', command=stop_temp_monitor, bg='red', fg='white', font=('helvetica', 9, 'bold'))  # Converts the "start button" to an "exit button".

    read_temps(update_interval, label_gpu_temp, label_cpu_temp)


def read_temps(update_interval: float or int, label_gpu_temp: tk.Label, label_cpu_temp: tk.Label) -> None:
    """
    Reads the CPU and GPU temperature and updates the labels that display them at a given interval.

    :param update_interval: The interval with which the temperatures are updated.
    :param label_gpu_temp: Label that displays the GPU temperature. Needed as input since they are created in another function and to avoid using global variables/objects.
    :param label_cpu_temp: Label that displays the GPU temperature. Needed as input since they are created in another function and to avoid using global variables/objects.
    :return:
    """
    Timer(interval=update_interval, function=read_temps, args=(update_interval, label_gpu_temp, label_cpu_temp,)).start()  # The function will be executed after "interval" seconds, i.e. running the function that it's part of. Resulting in read_temps being called repeatedly until program is killed.

    try:
        gpu_temp_byte_string = subprocess.check_output("vcgencmd measure_temp", shell=True)  # Returns a byte string containing the GPU temperature.
        gpu_temp_full = gpu_temp_byte_string.decode("utf-8")  # Using decode() function to convert byte string to utf-8-string
        gpu_temp = gpu_temp_full.split("=")  # Formatting output further, extracting the GPU temperature from the string.
        gpu_temp = gpu_temp[1].split("'")
        gpu_temp = gpu_temp[0]
        gpu_temp_str = str(gpu_temp) + "\u2103"  # Turning to string and adding "degree celsius"

        cpu_temp_byte_string = subprocess.check_output("cat /sys/class/thermal/thermal_zone0/temp", shell=True)  # Returns a byte string containing the CPU temperature.
        cpu_temp_1000 = cpu_temp_byte_string.decode("utf-8")  # Returns the CPU temperature multiplied by 1000.
        cpu_temp = round(int(cpu_temp_1000) / 1000, 1)  # Rounding CPU temperature to 1 decimal.
        cpu_temp_str = str(cpu_temp) + "\u2103"

        label_gpu_temp.config(text="GPU temperature: " + gpu_temp_str)
        label_cpu_temp.config(text="CPU temperature: " + cpu_temp_str)

    except RuntimeError:  # To handle if monitor is not closed with "Close monitor button".
        stop_temp_monitor()


def stop_temp_monitor() -> None:
    """
    To kill thread started by Timer.
    """
    os.kill(os.getpid(), signal.SIGTERM)


root = tk.Tk()
canvas = tk.Canvas(root, width=320, height=160, relief='raised')
canvas.pack()
root.title("Temperature Monitor")

label_entry = tk.Label(root, text='Enter update interval in seconds ("5" if left blank):')
label_entry.config(font=('helvetica', 10))
canvas.create_window(160, 20, window=label_entry)

entry_update_interval = tk.Entry(root)
entry_update_interval.focus()
canvas.create_window(160, 40, width=80, window=entry_update_interval)

button = tk.Button(text='Start temperature monitoring of GPU and CPU', command=temp_monitor, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
canvas.create_window(160, 70, window=button)

root.mainloop()
