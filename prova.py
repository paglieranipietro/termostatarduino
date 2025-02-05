import dearpygui.dearpygui as dpg
from math import sin, cos
import multiprocessing as mp
import random
import serial as ser
import time
import json

dpg.create_context()

# creating data
xs = []
ys = []
ys1 = []
ys2 = []

def update_zoom():
    if xs:
        min_x = min(xs)
        max_x = max(xs)
        dpg.set_axis_limits("x_axis", min_x-5, max_x)  # Margine di 5

    if ys:
        min_y = min(min(ys1), min(ys2))
        max_y = max(max(ys1), max(ys2))
        dpg.set_axis_limits("y_axis", min_y - 10, max_y + 10)  # Margine di 5


def update_data_callback():
    if not q.empty():
        line = q.get()
        if line:
            if len (xs) >= 19:
                ys.pop(0)
                ys1.pop(0)
                ys2.pop(0)

            temperature = float(line["temp"])
            ys.append(temperature)
            if len(xs) < 20:
                xs.append(len(ys)-1)
            dpg.set_value("temperature_series", [xs, ys])
            ys1.append(temperature + random.uniform(0.3, 0.5))  # Thinner upper bound
            ys2.append(temperature - random.uniform(0.3, 0.5))  # Thinner lower bound
            dpg.set_value("shaded_area", [xs, ys1, ys2])


def serial_task(q: mp.Queue):
    try:
        arduino = ser.Serial("COM5", 9600)
    except ser.SerialException as e:
        print(f"Error: {e}")
        return

    while True:
        line = arduino.readline()
        line = line.decode("utf-8")
        msg = json.loads(line)
        print(msg)
        q.put(msg)

if __name__ == "__main__":
    mp.freeze_support()
    q = mp.Queue()  # create the queue
    p = mp.Process(target=serial_task, args=(q,))
    p.start()

    with dpg.window(label="Termostato"):
        # create plot
        # Creazione degli assi
        with dpg.plot(label="Shaded Plot", tag="shaded_plot_1", width=800, height=500):
            x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis")
            y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis")
            dpg.add_shade_series(xs, ys1, y2=ys2, label="Shaded Area", tag="shaded_area", parent=y_axis)
            dpg.add_line_series(xs, ys, label="Function", tag="temperature_series", parent=y_axis)

        # Imposta i limiti dello zoom
        dpg.set_axis_limits("x_axis", 0, 20)  # Limiti dell'asse X
        dpg.set_axis_limits("y_axis", 0, 30)  # Limiti dell'asse Y

    dpg.create_viewport(title='Termostato', width=1400, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        update_data_callback()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
    p.terminate()
    p.join()
