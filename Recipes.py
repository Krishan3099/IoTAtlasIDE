import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import csv

services = []
relationships = []
alive = []

class Recipes(Frame):
    def __init__(self, parent, controller):
        from startpage import StartPage
        Frame.__init__(self, parent)
        with open('ApplicationServices.csv', 'r') as file:
            r = csv.reader(file)
            self.rows = [line for line in r]
        with open('relationship.csv', 'r') as file:
            rr = csv.reader(file)
            rr_rows = [line for line in rr]
            rr_rows = rr_rows[1:]

        viewWindow = ttk.Treeview(self, height=6, show="attributes", columns="Services listed")
        viewWindow.column("Services provided", width=300, anchor='center')
        viewWindow.heading("Services provided", text="Services provided")
        viewWindow.place(x=0, y=0)

        viewWindow2 = ttk.Treeview(self, height=6, show="attributes", columns="Relationships listed")
        viewWindow2.column("Relationships provided", width=300, anchor='center')
        viewWindow2.heading("Relationships provided", text="Relationships provided")
        viewWindow2.place(x=255, y=0)

        clist = ttk.Combobox(self)
        id = [line[0] for line in self.rows]
        clist["values"] = ["default"] + id
        clist.current(0)
        clist.place(x=550, y=12)
        clist.bind("<<ComboboxSelected>>", lambda event: self.initialize_service(viewWindow, clist))

        clist1 = ttk.Combobox(self)
        id = [line[0] for line in rr_rows]
        clist1["values"] = ["default"] + id
        clist1.current(0)
        clist1.place(x=550, y=55)
        clist1.bind("<<ComboboxSelected>>", lambda event: self.initialize_relationship(viewWindow2, clist1))

        btn1 = Button(self, text="okay", command=lambda : self.okayService(viewWindow, viewWindow2))
        btn1.place(x=550, y=260)
        btn2 = Button(self, text="Delete All", command=lambda: self.clear(viewWindow, viewWindow2))
        btn2.place(x=550, y=290)
        btn3 = Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        btn3.place(x=550, y=320)

    def initialize_service(self, ser, combinationBox):
        global services
        global alive
        if combinationBox.get() != "default":
            for line in self.rows:
                if line[0] == combinationBox.get()
                    if line[1] not in alive:
                        alive += [line[1]]
                    services += [combinationBox.get()]
                    ser.insert('', len(services)-1, values=(services[len(services)-1]))
                    break

    def initialize_relationship(self, ser, combinationBox):
        global relationships
        if combinationBox.get() not in relationships and combinationBox.get() != "default":
            relationships += [combinationBox.get()]
            ser.insert('', len(relationships) - 1, values=(relationships[len(relationships) - 1]))

    def clear(self, ser, rel):
        global services
        global relationships
        for i in ser.get_children():
            ser.delete(i)
        for i in rel.get_children():
            rel.delete(i)
        services = []
        relationships = []


    def okayService(self, ser, rel):
        global services
        global relationships
        serviceText = ''
        relationshipText = ''
        for i in services:
            serviceText += i + ','
        for i in relationships:
            relationshipText += i + ','
        relationshipText = relationshipText[:-1]
        file = open('okayService.txt', 'w')
        file.write(serviceText)
        file.write('\n')
        file.write(relationshipText)
        file.close()
        self.clear(ser, rel)

