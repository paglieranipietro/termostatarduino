import multiprocessing as mp
import serial as sr
import json

def serial_task(q: mp.Queue, port: str):
    arduino = sr.Serial(port, 9600)
    while True:
        line = arduino.readline()
        line = line.decode("utf-8")
        msg = {}
        msg = json.loads(line)
        q.put(msg)

def app():
    while True:
        data = {}
        if not q.empty():
            data = q.get()
            print(data)


if __name__ == "__main__":
    port = "COM" + str(input("Enter serial port number: "))
    mp.freeze_support()
    q = mp.Queue() # creo la coda
    p = mp.Process(target=serial_task,args=(q, port))
    p.start()
    app()