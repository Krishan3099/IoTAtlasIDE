from tkinter import *
import tkinter.ttk as ttk
import csv

LARGE_FONT = ("Verdana", 12)


class Things(Frame):
    def __init__(self, parent, controller):
        from startpage import StartPage
        Frame.__init__(self, parent)

        self.cols = ('Smart Space Thing Name', 'Thing IP Address')
        self.treeview = ttk.Treeview(self, columns=self.cols, height=5)
        self.treeview.grid(row=0, column=0, sticky=NSEW)

        self.treeview.heading('#1', text='Thing Name', anchor='center')
        self.treeview.heading('#2', text='Thing IP Address', anchor='center')

        style = ttk.Style(self)
        style.configure('Treeview', rowheight=80)

        with open('thing.csv', 'r') as file:
            reader = csv.reader(file)
            rows = [row for row in reader]
        for i in range(len(rows)):
            self.treeview.insert('', 'end', value=(rows[i][0], rows[i][1]))

        # add back button
        btn = Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        btn.place(x=650, y=400)
