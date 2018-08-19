#!flask/bin/python
from flask import Flask
import time
import threading
import random

app = Flask(__name__)

def aggiorna1():
    global value1
    value1 = 0
    while True:
        time.sleep(5)
        value1 += 1

def aggiorna2():
    global value2
    value2 = 0
    while True:
        time.sleep(15)
        value2 += 1

@app.route('/')
def home():
    return "Ciao"

@app.route('/bar1')
def bar1():
    return str(value1)

@app.route('/bar2')
def bar2():
    return str(value2)

if __name__ == '__main__':
    threading.Thread(target=aggiorna1).start()
    threading.Thread(target=aggiorna2).start()
    app.run(host='0.0.0.0', port=4000, threaded=True)