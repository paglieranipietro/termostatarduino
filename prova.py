import dearpygui.dearpygui as dpg
import multiprocessing as mp
import random
import serial as ser
import json
import datetime

dpg.create_context()

# creating data
xs = []
ys_temp = []
ys_humid = []
ys1_temp = []
ys2_temp = []
ys1_humid = []
ys2_humid = []


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
        min_x = min(xs)
        max_x = max(xs)
        dpg.set_axis_limits("x_axis_temp", min_x - 5, max_x)
        dpg.set_axis_limits("x_axis_humid", min_x - 5, max_x)

    if ys_temp and ys_humid:
        min_y_temp = min(min(ys1_temp), min(ys2_temp))
        max_y_temp = max(max(ys1_temp), max(ys2_temp))
        min_y_humid = min(min(ys1_humid), min(ys2_humid))
        max_y_humid = max(max(ys1_humid), max(ys2_humid))
        dpg.set_axis_limits("y_axis_temp", min_y_temp - 10, max_y_temp + 10)
        dpg.set_axis_limits("y_axis_humid", min_y_humid - 10, max_y_humid + 10)


def update_data_callback():
    if not q.empty():
        line = q.get()
        if line:
            if len(xs) >= 19:
                ys_temp.pop(0)
                ys_humid.pop(0)
                ys1_temp.pop(0)
                ys2_temp.pop(0)
                ys1_humid.pop(0)
                ys2_humid.pop(0)

            temperature = float(line["temp"])
            humidity = float(line["umid"])
            ys_temp.append(temperature)
            ys_humid.append(humidity)

            if len(xs) < 20:
                xs.append(len(ys_temp) - 1)

            dpg.set_value("temperature_series", [xs, ys_temp])
            dpg.set_value("humidity_series", [xs, ys_humid])

            ys1_temp.append(temperature + random.uniform(0.3, 0.5))
            ys2_temp.append(temperature - random.uniform(0.3, 0.5))
            ys1_humid.append(humidity + random.uniform(0.3, 0.5))
            ys2_humid.append(humidity - random.uniform(0.3, 0.5))

            dpg.set_value("shaded_area_temp", [xs, ys1_temp, ys2_temp])
            dpg.set_value("shaded_area_humid", [xs, ys1_humid, ys2_humid])

            salva_dati(temperature, humidity)
            update_zoom()


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
    q = mp.Queue()
    p = mp.Process(target=serial_task, args=(q,))
    p.start()

    with dpg.window(label="Termostato"):
        with dpg.plot(label="Temperatura", tag="shaded_plot_temp", width=800, height=300):
            x_axis_temp = dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis_temp")
            y_axis_temp = dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis_temp")
            dpg.add_shade_series(xs, ys1_temp, y2=ys2_temp, label="Shaded Area", tag="shaded_area_temp",
                                 parent=y_axis_temp)
            dpg.add_line_series(xs, ys_temp, label="Temperatura", tag="temperature_series", parent=y_axis_temp)

        with dpg.plot(label="Umidità", tag="shaded_plot_humid", width=800, height=300):
            x_axis_humid = dpg.add_plot_axis(dpg.mvXAxis, label="x", tag="x_axis_humid")
            y_axis_humid = dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="y_axis_humid")
            dpg.add_shade_series(xs, ys1_humid, y2=ys2_humid, label="Shaded Area", tag="shaded_area_humid",
                                 parent=y_axis_humid)
            dpg.add_line_series(xs, ys_humid, label="Umidità", tag="humidity_series", parent=y_axis_humid)

    dpg.create_viewport(title='Termostato', width=1400, height=800)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    while dpg.is_dearpygui_running():
        update_data_callback()
        dpg.render_dearpygui_frame()

    dpg.destroy_context()
    p.terminate()
    p.join()
