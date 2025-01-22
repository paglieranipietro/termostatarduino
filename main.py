import multiprocessing as mp
import serial as sr
import json

data = 0

def serial_task(q: mp.Queue):
    arduino = sr.Serial("COM6", 9600)
    while True:
        line = arduino.readline().strip()
        line = line.decode("utf-8")
        msg = json.load(line)
        q.put(msg)

def app():
    global data
    min_gradi = 20
    min_y = 400
    max_gradi = 30
    max_y = 50
    x = 170


    # init_window(800, 450, "Hello")
    # while not window_should_close():
        #if not q.empty():
            #data = q.get()
        #begin_drawing()

        #clear_background(WHITE)


        # temp = data["temp"]
        # draw_text(f"data = {temp}", 190, 200, 20, VIOLET)
        # draw_line(x, min_y, x, max_y, RED)

        # y = int( ((data - min_gradi) * (max_y - min_y)) / (max_gradi - min_gradi) )
        # draw_circle(x, y + min_y, 10, RED)

        #end_drawing()

    #close_window()

if __name__ == "__main__":
    mp.freeze_support()
    q = mp.Queue() # creo la coda
    p = mp.Process(target=serial_task,args=(q,))
    p.start()
    app()