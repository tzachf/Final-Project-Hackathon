import serial
import time
import requests
import os
import pandas as pd
from pywinauto import application
from pywinauto.win32functions import ShowWindow
from pynput.keyboard import Key, Controller
from tkinter import *
from datetime import datetime
import tkinter.font as font
ser = serial.Serial('COM4', 9600, timeout=1)
PATIENT_NAME = ""
window=Tk()

def pepperReactionLogics(compensations):
    # TODO: Pepper Reaction based on compensations
    print("DASDASD")


def startGame(patient_name):
    PATIENT_NAME = patient_name
    window.withdraw()
    # pepper_start_game_reaction = {'Pepper Reaction': 'Start Game'}
    # r = requests.post('http://10.0.0.7:3333/react/', data=pepper_start_game_reaction)

    # TODO: Pepper Reaction

    # Start Recording

    app = application.Application().connect(path=r"C:\Program Files\OptiTrack\Motive\Motive.exe")
    w = app.top_window()

    # Open Motive App
    ShowWindow(w.wrapper_object(), 9)
    time.sleep(1)
    keyboard = Controller()
    # Change to Live Mode
    keyboard.press('3')
    time.sleep(0.7)
    # Press space to start recording
    keyboard.press(Key.space)

    print("waiting for button1")
    ser.write(b'o')
    arduinodata1 = ser.readlines()
    ser.write(b'o')
    arduinodata1 = ser.readlines()
    print("button pressed")

    keyboard.press(Key.space)

    # Change to Edit mode in Motive
    keyboard.press('4')

    # Export file to csv
    time.sleep(1)
    file_to_analyze_name = PATIENT_NAME + datetime.now().strftime("%H:%M:%S")
    keyboard.press('5')
    print(file_to_analyze_name)
    # Set csv file to patient name + exercise datetime
    time.sleep(1)
    for i in range(len(file_to_analyze_name)):
        keyboard.press(file_to_analyze_name[i])
        time.sleep(0.01)
    time.sleep(1)
    keyboard.press(Key.enter)
    time.sleep(13 )
    keyboard.press(Key.enter)
    file_to_analyze_name = file_to_analyze_name.replace(":", "_")
    file_to_analyze_name = file_to_analyze_name.replace("\"", "\\")
    path = "C:\\Users\\dafnanet\\Documents\\Hackton\\CompensationApp\\Movements\\" + file_to_analyze_name + ".csv"
    # Open csv file and send to server in order to analyze
    print(path)

    time.sleep(2)
    # file = pd.read_csv(path)
    files = {'file': open(path)}
    r= requests.post('http://127.0.0.1:8000/analyze/', files=files)
    #
    # # Get predictions from the algorithm
    # predictions = r.json()

    # Operate Pepper according to predictions
    # pepperReactionLogics(predictions)
    print("SUCCESS")

myFont = font.Font(family='Bahnschrift Light', size=14, weight='bold')
lbl=Label(window, text="Please enter your name:", fg='red', font=myFont)
lbl.place(x=50, y=50)
txtfld=Entry(window, text="This is Entry Widget", bd=5)
txtfld.place(x=82, y=90)
btn=Button(window, text="Start game!", fg='red',bg='white',font=myFont,command=lambda: startGame(txtfld.get()))
btn.place(x=85, y=150)

window.configure(background='black')
window.title('Pepper - social robot')
window.geometry("300x200+10+10")
window.mainloop()

# patient_name_entry = Entry(root, width=20, borderwidth=5)
# patient_name_entry.insert(0, "Please Enter Your Name:")
# patient_name_entry.pack()
# start_game_button = Button(root, text="Start Game", command=lambda: startGame(patient_name_entry.get()))
# start_game_button.pack()
# root.mainloop()


class Tags(object):
    def __init__(self):
        self.running = True
        self.threads = []

    def getValues(self, q, LevelNumber):  # checks the order of the cups
        arduinodata1 = [];
        arduinodata = []
        #        ser.open()
        ser.write(b'o')
        arduinodata1 = ser.readlines()
        arduinodata1 = (x for x in arduinodata1 if
                        "Reader" in x)
        # delete all the unessery data that was in the serial
        arduinodata1 = [i.split('\r\n', 1)[0] for i in arduinodata1]
        ser.write(b'o')
        arduinodata1 = ser.readlines()
        print("push")

        # START RECORDING

        # dsock = rx.mkdatasock()
        # version = (3, 1, 0, 0)  # NatNet version to use
        # while True:
        #     data = dsock.recv(rx.MAX_PACKETSIZE)
        #     print data
        #     print ("1")
        #     packet = rx.unpack(data, version=version)
        #     if type(packet) is rx.SenderData:
        #         version = packet.natnet_version
        #     print packet
        ser.write(b'o')
        arduinodata1 = ser.readlines()
        arduinodata1 = (x for x in arduinodata1 if
                        "Reader" in x)
        # delete all the unessery data that was in the serial
        arduinodata1 = [i.split('\r\n', 1)[0] for i in arduinodata1]
        ser.write(b'o')
        arduinodata1 = ser.readlines()
        print("push2")

        # END RECORDING AND SEND TO ALGORITHM


q = []
tag = Tags()

tag.getValues(q, 2)
