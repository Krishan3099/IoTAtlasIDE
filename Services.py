from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
import  csv
import collections
import tkinter.messagebox
class Services(Frame):
    def __init__(self, parent,rows):
        Frame.__init__(self, parent)
        self.setup()
        self.loadup(rows)
        self.grid(sticky = (N,S,W,E))
        parent.rowGrid(0, weight = 1)
        parent.colGrid(0, weight = 1)
        style = Style(parent)
        style.configure('Treeview', rowheight=100)

    def setup(self):
        treeview = Treeview(self)
        treeview['columns'] = ('Index', 'end')
        treeview.heading("#0", text='Service Name', anchor='w')
        treeview.column("#0", anchor="w")
        treeview.heading('Index', text='Thing ID')
        treeview.column('Index', anchor='center', width=100)
        treeview.grid(sticky = (N,S,W,E))
        self.treeview = treeview
        self.rowGrid(0, weight = 1)
        self.colGrid(0, weight = 1)

    def loadup(self,details):
        garbage = []
        cnt=0
        cnt_image = 0
        for d in details:
            for element in details[d]:
                self.treeview.insert('', 'end', text=str(element[0]), values=(d))


def filter(*args):
    global key
    global key1
    global app2
    global app
    global clist
    global clist2
    global clist1
    if clist:
        key = clist.get()
        if key != 'default':
            if app:
                app.destroy()
            if app2:
                app2.destroy()
            buffer={}
            buffer[key]=buffer.get(key,[])+data[key]
            app2=Services(root, buffer)
            clist = ttk.Combobox(root)
            clist["values"] = ["default"] + id
            clist.current(0)
            clist.place(relx = 0.640, rely = 0.001)
            clist.bind("<<ComboboxSelected>>", filter)
        # else:
        #     tkinter.messagebox.showinfo('Error','Please select an appropiate item!')


root = Tk()
with open('service.csv', 'r') as file:
    reader = csv.reader(file)
    rows = [row for row in reader]
data=collections.defaultdict(list)
for r in rows:
    data[r[1]].append([r[0]])
id = list(set([row[1] for row in rows]))
image = []
image_dict = {}
key=None
key1=None
app2=None
app=None
clist1=None
clist=None
app=Services(root,data)
clist = ttk.Combobox(root)
clist["values"] = ["default"]+id
clist.current(0)
clist.place(relx = 0.640, rely = 0.001)
clist.bind("<<ComboboxSelected>>",filter)
root.mainloop()
