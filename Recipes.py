import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import csv

LARGE_FONT = ("Verdana", 12)


servicesInfo = []
relationshipInfo = []
alive = []


class Recipe(Frame):
    def __init__(self, parent, controller):
        print("Recipe")
        from startpage import StartPage
        Frame.__init__(self, parent)

        with open('service.csv', 'r') as file:
            reader = csv.reader(file)
            self.rows = [row for row in reader]
        with open('relationship.csv', 'r') as file:
            reader_array = csv.reader(file)
            rowsArray = [row for row in reader_array]
            rowsArray = rowsArray[1:]
        servicesTree = ttk.Treeview(self, height=5, show="headings", columns=("Services"))
        servicesTree.column("Services", width=220, anchor='center')
        servicesTree.heading("Services", text="Services")
        servicesTree.place(x=0, y=0)
        bar1 = ttk.Scrollbar(servicesTree, orient='vertical',command=servicesTree.yview)
        bar1.place(relx=0.91, rely=0.02, relwidth=0.08, relheight=0.95)
        servicesTree.configure(yscrollcommand=bar1.set)

        relationshipTree = ttk.Treeview(self, height=5, show="headings", columns=("Relationships"))
        relationshipTree.column("Relationships", width=220, anchor='center')
        relationshipTree.heading("Relationships", text="Relationships")
        relationshipTree.place(x=250, y=0)
        bar2 = ttk.Scrollbar(relationshipTree, orient='vertical',command=relationshipTree.yview)
        bar2.place(relx=0.91, rely=0.02, relwidth=0.08, relheight=0.95)
        clist = ttk.Combobox(self)
        id = [row[0] for row in self.rows]
        clist["values"] = ["default"] + id
        clist.current(0)
        clist.place(x=600, y=15)
        clist.bind("<<ComboboxSelected>>", lambda event: self.add_service(servicesTree, clist))

        clist1 = ttk.Combobox(self)
        id = [row[0] for row in rowsArray]
        clist1["values"] = ["default"] + id
        clist1.current(0)
        clist1.place(x=600, y=60)
        clist1.bind("<<ComboboxSelected>>", lambda event: self.add_relationship(relationshipTree, clist1))

        # buttons
        btnFinalize = Button(self, text='okay',command=lambda: self.finalize_app(servicesTree, relationshipTree))
        btnFinalize.place(x=600, y=270)

        btnclear = Button(self, text='Delete all', command=lambda: self.clear_all(servicesTree, relationshipTree))
        btnclear.place(x=600, y=300)

        btnback = Button(self, text="Back", command=lambda: controller.show_frame(StartPage))
        btnback.place(x=600, y=330)


    def add_service(self, treeViewService, comb0):
        global servicesInfo, alive
        if comb0.get() != "default":
            for row in self.rows:
                if row[0] == comb0.get():
                    if row[1] not in alive:
                        alive += [row[1]]
                    servicesInfo += [comb0.get()]
                    treeViewService.insert('', len(servicesInfo) - 1, values=(servicesInfo[len(servicesInfo) - 1]))
                    break
        # else:
        #     tkinter.messagebox.showinfo('Error', 'Please select an appropriat thing!')


    def add_relationship(self, treeViewRelationship, comb1):
        print("b")
        global relationshipInfo
        if comb1.get() not in relationshipInfo and comb1.get() != "default":
            relationshipInfo += [comb1.get()]
            treeViewRelationship.insert('', len(relationshipInfo) - 1, values=(relationshipInfo[len(relationshipInfo) - 1]))
        # elif comb1.get() == "default":
        #     tkinter.messagebox.showinfo('Error', 'Please select an appropriate thing!')
        # else:
        #     tkinter.messagebox.showinfo('Error', 'Can not add same thing!')

    def clear_all(self, treeViewService, treeViewRelationship):
        global servicesInfo, relationshipInfo
        for thing in treeViewService.get_children():
            treeViewService.delete(thing)
        for thing in treeViewRelationship.get_children():
            treeViewRelationship.delete(thing)
        servicesInfo, relationshipInfo = [], []

    def finalize_app(self, treeViewService, treeViewRelationship):
        global servicesInfo, relationshipInfo
        service, relationship = '', ''
        for thing in servicesInfo:
            service += thing + ','
        service = service[:-1]
        for thing in relationshipInfo:
            relationship += thing +','
        relationship = relationship[:-1]
        f = open("recipe.txt", 'w')
        f.write(service)
        f.write('\n')
        f.write(relationship)
        f.close()
        self.clear_all(treeViewService, treeViewRelationship)