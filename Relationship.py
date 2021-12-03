from tkinter import *
import pandas as pd
from tkinter import ttk
import csv

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Relationships")

        global count
        count=0
        df = pd.DataFrame(pd.read_csv('relationship.csv'))
        columns = list(df.columns)
        self.treeview = ttk.Treeview(self)
        self.combo = ttk.Combobox(self, postcommand = self.refresh, state="readonly")
        self.combo.pack()
        self.combo.bind("<<ComboboxSelected>>", self.dropDown)
        self.treeview["columns"] = columns
        self.treeview.pack(expand=TRUE, fill=BOTH)

        for i in columns:
            self.treeview.column(i, anchor="w")
            self.treeview.heading(i, text=i, anchor="w")

        self.scroll = Scrollbar(self, orient='vertical', command=self.treeview.yview)
        self.scroll.place(relx=0.971, rely=0.028, relwidth=0.024, relheight=0.958)
        self.scroll2 = Scrollbar(self, orient='horizontal', command=self.treeview.xview)
        self.scroll2.place(relx=0.028, rely=0.971, relwidth=0.958, relheight=0.024)
        #add configuration to treeview
        self.treeview.configure(yscrollcommand=self.scroll.set)
        self.treeview.configure(xscrollcommand=self.scroll2.set)

        self.treeview.bind('<Double-1>', func = self.setup)
        self.create = ttk.Button(self, text="Create New Relationship", command=self.newrow)
        self.create.pack(expand = 1)
        df = pd.DataFrame(pd.read_csv('relationship.csv'))
        rows = len(list(df.index))
        print(df)
        a = df["Name"]
        b = df["Type"]
        c = df["Service1"]
        d = df["Service2"]
        for i in range(0, len(df.index)):
            self.treeview.insert('', "end", text=i+1, values=[a[i], b[i], c[i], d[i]])
            self.treeview.update()

    def refresh(self):
        df = pd.DataFrame(pd.read_csv('Relationship.csv'))
        self.combo['values'] = [""] + list(df["Type"].unique())

    def setup(self,event):
        for item in self.treeview.selection():
            item_text = self.treeview.item(item, "values")
        column = self.treeview.identify_column(event.x)  #colum
        entryedit = Text(root, width=10, height=1)
        entryedit.place(x=220, y=300)
        def update():
            self.treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
            entryedit.destroy()
            okb.destroy()
            self.saveFile()
        okb = ttk.Button(root, text='OK', width=4, command=update)
        okb.place(x=300, y=290)

    def newrow(self):
        global count



    def dropDown(self,event=None):
        df = pd.DataFrame(pd.read_csv('relationship.csv'))
        self.treeview.delete(*self.treeview.get_children())
        cnt = 0
        for index, row in df.loc[df["Type"].eq(self.combo.get())].iterrows():
            self.treeview.insert("", "end", text=index, values=list(row))
            cnt = cnt +1
        if cnt == 0:
            for index, row in df.iterrows():
                self.treeview.insert("", "end", text=index, values=list(row))

    def saveFile(self):
        with open("relationship.csv", "w", newline='') as file:
            csvfile = csv.writer(file, delimiter=',')
            csvfile.writerow(['Name','Type','Service1','Service2'])

            for row_id in self.treeview.get_children():
                row = self.treeview.item(row_id)['values']
                print('save row:', row)
                csvfile.writerow(row)

root = Application()
root.geometry('600x400')
root.mainloop()