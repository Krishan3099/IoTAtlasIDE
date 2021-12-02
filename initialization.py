import tkinter as tk
from tkinter import ttk
import time
import tkinter.messagebox
import os
import queue
import struct
import socket
import threading
import select
from startpage import StartPage

thing = 0
ip_array = []
name = ''
flag = False
count = 1

class Initialization(tk.Frame):
    def __init__(self, parent, controller):
        global thing
        global ip_array

        tk.Frame.__init__(self, parent)
        self.queue = queue.Queue()
        ip_array = ''
        label = tk.Label(self, text="Name: ")
        label.place(x=10, y=10)
        self.nameName=tk.Entry(self, relief=tk.RIDGE)
        self.nameName.place(x=200, y=20)

        label2 = tk.Label(self, text="Number of Things: ")
        label2.place(x=10, y=50)
        self.thingName = tk.Entry(self, width=65, relief=tk.RIDGE)
        self.thingName.place(x=20, y=100)

        self.label3 = tk.Label(self, text="Click on start ")
        self.label3.place(x=10, y=100)
        self.progress = ttk.Progressbar(self, orient='vertical', length=320, mode='determinate')
        self.button = tk.Button(self, text="start", command = lambda : self.start(controller))
        self.button.place(x=400, y=200)
        self.progress.place(x=300, y=200)

    def start(self, controller):
        global thing
        global count
        global ip_array
        global name
        global flag
        good = True
        things = []
        name = self.nameName.get()
        thing = self.thingName.get()
        if good:
            count = int(thing)
            thing = int(thing)
            self.button.config(state="disabled")
            self.thd = User(self.queue)
            self.multiple()

            self.label3['text'] = "Running"
            self.button['command'] = lambda : controller.show_frame(StartPage)

    def multiple(self):
        self.checkup()
        self.button.config(state = "active")
        if flag:
            self.label3['text'] = "Incorrect input"
            self.label3['text'] = "log out"
            self.button['command'] = lambda:Initialization.quit(self)

    def checkup(self):
        global count
        while self.queue.qsize():
            tweet = self.queue.get(0)
            self.progress['value'] += 100 / count

class User(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue






