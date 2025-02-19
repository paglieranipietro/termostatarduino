import time

import dearpygui.dearpygui as dpg
import multiprocessing as mp
import random
import serial as ser
import json
import datetime

from dearpygui.dearpygui import add_text
from screeninfo import get_monitors

dpg.create_context()

# creating data
xs = []
ys_temp = []
ys_humid = []
ys1_temp = []
ys2_temp = []
ys1_humid = []
ys2_humid = []
MAX_WIDTH = get_monitors()[0].width
MAX_HEIGHT = get_monitors()[0].height

start = time.time()

def salva_dati(temp, umid, filename="dati_temperatura.json"):
    nuovo_dato = {
        "data": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temp": temp,
        "umid": umid
    }
    try:
        with open(filename, "a") as file:
            file.write(json.dumps(nuovo_dato) + "\n")
    except Exception as e:
        print(f"Errore durante il salvataggio dei dati: {e}")


def update_zoom():
    if xs:
        min_x = xs[0]
        max_x = xs[len(xs) - 1]
        dpg.set_axis_limits("x_axis_temp", min_x, max_x)
        dpg.set_axis_limits("x_axis_humid", min_x, max_x)

    if ys_temp and ys_humid:
        min_y_temp = min(min(ys1_temp), min(ys2_temp))
        max_y_temp = max(max(ys1_temp), max(ys2_temp))
        min_y_humid = min(min(ys1_humid), min(ys2_humid))
        max_y_humid = max(max(ys1_humid), max(ys2_humid))
        dpg.set_axis_limits("y_axis_temp", min_y_temp - 5, max_y_temp + 5)
        dpg.set_axis_limits("y_axis_humid", min_y_humid - 5, max_y_humid + 5)


def update_data_callback():
    if not q.empty():
        line = q.get()
        if line:
            if len(xs) >= 20:
                ys_temp.pop(0)
                ys_humid.pop(0)
                ys1_temp.pop(0)
                ys2_temp.pop(0)
                ys1_humid.pop(0)
                ys2_humid.pop(0)
                xs.pop(0)

            temperature = float(line["temp"])
            humidity = float(line["umid"])

            if len(xs) < 20:
                xs.append(time.time() - start)
                ys_temp.append(temperature)
                ys_humid.append(humidity)

            dpg.set_value("temperature_series", [xs, ys_temp])
            dpg.set_value("humidity_series", [xs, ys_humid])

            ys1_temp.append(temperature + random.uniform(0.3, 0.5))
            ys2_temp.append(temperature - random.uniform(0.3, 0.5))
            ys1_humid.append(humidity + random.uniform(0.3, 0.5))
            ys2_humid.append(humidity - random.uniform(0.3, 0.5))

            dpg.set_value("temp_text", str(round(temperature, 2)) + "°C")

            salva_dati(temperature, humidity)
            update_zoom()

            # Aggiornamento LED

            led1 = bool(line["led1"])
            led2 = bool(line["led2"])

            if led1:
                dpg.configure_item("led1", fill=(0, 255, 0))
            else:
                dpg.configure_item("led1", fill=(0, 30, 0))

            if led2:
                dpg.configure_item("led2", fill=(255, 0, 0))
            else:
                dpg.configure_item("led2", fill=(30, 0, 0))


def serial_task(q: mp.Queue, com):
    try:
        arduino = ser.Serial("COM" + com, 9600)
    except ser.SerialException as e:
        print(f"Error: {e}")
        return

    while True:
        line = arduino.readline()
        line = line.decode("utf-8")
        msg = json.loads(line)
        print(msg)
        q.put(msg)

def test_data(q: mp.Queue):
    num_temp = 25
    num_humid = 60
    while True:
        msg = {"temp":random.uniform(num_temp - 3, num_temp + 3), "umid":random.uniform(num_humid - 10,num_humid + 10), "led1":random.choice([False, True]), "led2":random.choice([False, True])}
        print(msg)
        q.put(msg)
        time.sleep(2)


if __name__ == "__main__":
    com = input("Inserire il numero della COM: ")

    mp.freeze_support()
    q = mp.Queue()
    if com == "TEST":
        t = mp.Process(target=test_data, args=(q,))
        t.start()
    else:
        p = mp.Process(target=serial_task, args=(q,com))
        p.start()

    with dpg.window(label="Termostato", tag="main_window"):
        dpg.set_primary_window("main_window", True)
        with dpg.plot(label="Temperatura", tag="shaded_plot_temp", width=1200, height=500):
            x_axis_temp = dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis_temp")
            y_axis_temp = dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis_temp")
            dpg.add_shade_series(xs, ys1_temp, y2=ys2_temp, label="Shaded Area", tag="shaded_area_temp",
                                 parent=y_axis_temp)
            dpg.add_line_series(xs, ys_temp, label="Temperatura", tag="temperature_series", parent=y_axis_temp)

        with dpg.plot(label="Umidità", tag="shaded_plot_humid", width=1200, height=500):
            x_axis_humid = dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis_humid")
            y_axis_humid = dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis_humid")
            dpg.add_shade_series(xs, ys1_humid, y2=ys2_humid, label="Shaded Area", tag="shaded_area_humid",
                                 parent=y_axis_humid)
            dpg.add_line_series(xs, ys_humid, label="Umidità", tag="humidity_series", parent=y_axis_humid)

        with dpg.window(label="Stato LED temperatura", pos=(1300, 0), width=300, height=150):
            dpg.draw_circle((100, 40), 30, color=(0, 0, 0), fill=(0, 30, 0), tag="led1")
            dpg.draw_circle((200, 40), 30, color=(0, 0, 0), fill=(30, 0, 0), tag="led2")

        with dpg.window(label="temp_value", pos=(1300, 200), width=300, height=150):
            add_text("0°C", pos=(), tag="temp_text", )

    dpg.create_viewport(title='Termostato')
    dpg.configure_viewport("Termostato", width=MAX_WIDTH, height=MAX_HEIGHT, always_on_top=True)
    dpg.set_viewport_pos([0,0])
    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        update_data_callback()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
    p.terminate()
    p.join()
