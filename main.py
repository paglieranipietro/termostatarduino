import multiprocessing as mp
import serial as ser
import json
import dearpygui.dearpygui as dpg
import threading
import time

def serial_task(q: mp.Queue):
    arduino = ser.Serial("COM5", 9600)
    while True:
        line = arduino.readline()
        line = line.decode("utf-8")
        msg = json.loads(line)
        q.put(msg)

# creating data
xs = [i * 0.001 for i in range(1001)]
ys = [0] * 1001
ys1 = []
ys2 = []

def update_data():
    while dpg.is_dearpygui_running():
        if not q.empty():
            data = q.get()
            temperature = float(data["temp"])
            ys.append(temperature)
            ys.pop(0)
            dpg.set_value("temperature_series", [xs, ys])
        time.sleep(1)  # Update every second

if __name__ == "__main__":
    mp.freeze_support()
    q = mp.Queue()  # create the queue
    p = mp.Process(target=serial_task, args=(q,))
    p.start()

    with dpg.window(label="Tutorial"):
        # create plot
        with dpg.plot(label="Shaded Plot", tag="shaded_plot_1", width=800, height=500):
            dpg.add_plot_axis(dpg.mvXAxis, label="x")
            with dpg.plot_axis(dpg.mvYAxis, label="y"):
                dpg.add_shade_series(xs, ys1, y2=ys2, label="Shaded Area", fill_color=(0, 0, 255, 100))
                dpg.add_line_series(xs, ys, label="Function", color=(0, 0, 255, 255), tag="temperature_series")

    dpg.create_viewport(title='Custom Title', width=1400, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    # Start the update thread
    update_thread = threading.Thread(target=update_data)
    update_thread.start()

    dpg.start_dearpygui()
    dpg.destroy_context()
    p.join()