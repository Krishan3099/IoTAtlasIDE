import tkinter.messagebox
from tkinter import *
from tkinter import ttk
import csv

LARGE_FONT = ("Verdana", 12)
<<<<<<< HEAD


servicesInfo = []
relationshipInfo = []
alive = []


=======


service_col = []
relationship_col = []
exist_thing = []


>>>>>>> c9fed05f635146bb51969f4213b27e06a0a51c5e
class Recipe(Frame):
    def __init__(self, parent, controller):
        print("Recipe")
        from startpage import StartPage
        Frame.__init__(self, parent)

<<<<<<< HEAD
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
=======
        with open('service.csv', 'r') as csvfile_service:
            reader = csv.reader(csvfile_service)
            self.rows = [row for row in reader]
        with open('relationship.csv', 'r') as csvfile_relation:
            reader_rela = csv.reader(csvfile_relation)
            rows_rela = [row for row in reader_rela]
            rows_rela = rows_rela[1:]
    
    
        treeview_service = ttk.Treeview(self, height=5, show="headings", columns=("Services"))
        treeview_service.column("Services", width=250, anchor='center')
        treeview_service.heading("Services", text="Services")
        treeview_service.place(x=0, y=0)
        roll1 = ttk.Scrollbar(treeview_service, orient='vertical',command=treeview_service.yview)
        
        roll1.place(relx=0.91, rely=0.02, relwidth=0.08, relheight=0.95)
        treeview_service.configure(yscrollcommand=roll1.set)

    
        treeview_relationship = ttk.Treeview(self, height=5, show="headings", columns=("Relationships"))
        treeview_relationship.column("Relationships", width=250, anchor='center')
        treeview_relationship.heading("Relationships", text="Relationships")
        treeview_relationship.place(x=250, y=0)
        roll2 = ttk.Scrollbar(treeview_relationship, orient='vertical',command=treeview_relationship.yview)
        
        roll2.place(relx=0.91, rely=0.02, relwidth=0.08, relheight=0.95)
        treeview_relationship.configure(yscrollcommand=roll2.set)
        
     
        
        comboxlist0 = ttk.Combobox(self) 
        id = [row[0] for row in self.rows]
        comboxlist0["values"] = ["default"] + id
        comboxlist0.current(0)
        comboxlist0.place(x=600, y=15)
        comboxlist0.bind("<<ComboboxSelected>>", lambda event: self.add_service(treeview_service, comboxlist0))
        comboxlist1 = ttk.Combobox(self) 
        id = [row[0] for row in rows_rela]
        comboxlist1["values"] = ["default"] + id
        comboxlist1.current(0)
        comboxlist1.place(x=600, y=60)
        comboxlist1.bind("<<ComboboxSelected>>", lambda event: self.add_relationship(treeview_relationship, comboxlist1))  

        button_Finalize = Button(self, text='Finalize',command=lambda: self.finalize_app(treeview_service, treeview_relationship))
        button_Finalize.place(x=600, y=270)

        button_clear = Button(self, text='Clear', command=lambda: self.clear_all(treeview_service, treeview_relationship))
        button_clear.place(x=600, y=300)

        button_back = Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
        button_back.place(x=600, y=330)


    def add_service(self, tv_service, comb0):
        global service_col, exist_thing
        if comb0.get() != "default":
            for row in self.rows:
                if row[0] == comb0.get():
                    if row[1] not in exist_thing:
                        exist_thing += [row[1]]
                    service_col += [comb0.get()]
                    tv_service.insert('', len(service_col) - 1, values=(service_col[len(service_col) - 1]))
                    break
        else:
            tkinter.messagebox.showinfo('Error', 'Select correct option!')
        
        


    def add_relationship(self, tv_reltship, comb1):
        print("b")
        global relationship_col
        if comb1.get() not in relationship_col and comb1.get() != "default":
            relationship_col += [comb1.get()]
            tv_reltship.insert('', len(relationship_col) - 1, values=(relationship_col[len(relationship_col) - 1]))
        elif comb1.get() == "default":
            tkinter.messagebox.showinfo('Error', 'Select correct option!')
        else:
            tkinter.messagebox.showinfo('Error', 'Same item not allowed!')

    def clear_all(self, tv_service, tv_reltship):
        global service_col, relationship_col
        for item in tv_service.get_children():
            tv_service.delete(item)
        for item in tv_reltship.get_children():
            tv_reltship.delete(item)
        service_col, relationship_col = [], []

    def finalize_app(self, tv_service, tv_reltship):
        global service_col, relationship_col
        service, relationship = '', ''
        for item in service_col:
            service += item + ','
        service = service[:-1]
        for item in relationship_col:
            relationship += item +','
        relationship = relationship[:-1]
        f = open("finalize_app.txt", 'w')
>>>>>>> c9fed05f635146bb51969f4213b27e06a0a51c5e
        f.write(service)
        f.write('\n')
        f.write(relationship)
        f.close()
<<<<<<< HEAD
        self.clear_all(treeViewService, treeViewRelationship)
=======
        self.clear_all(tv_service, tv_reltship)
>>>>>>> c9fed05f635146bb51969f4213b27e06a0a51c5e
