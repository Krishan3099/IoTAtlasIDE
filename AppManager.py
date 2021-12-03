import collections
from tkinter import *
from tkinter import ttk, scrolledtext
from tkinter import filedialog
from PIL import Image
import os
import csv
from itertools import islice
import socket
import time
import datetime
import pandas as pd
import threading

work_directory = './'

appname_log=collections.defaultdict(list)

class Application(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("App Manager")

        self.flag = 1

        self.menu = Menu(self)
        self['menu']=self.menu
        
        self.b_activate = ttk.Button(self, text="activate", command=self.activate)
        self.b_activate.pack(expand=1)
        self.b_status = ttk.Button(self, text="Status Panel", command=self.Status)
        self.b_status.pack(expand=1)


    def activate(self):
        spath = filedialog.asksaveasfilename(title='save', filetypes=[("TXT", ".txt")], initialdir = work_directory)
        if spath != '':
            spath1 = os.path.splitext(spath)
            filename = os.path.split(spath1[0])
            print(filename[1])
        
            full_path = spath + '.txt'

            
            f = open("finalize_app.txt", 'r')
            lines_file = f.readlines()
            services = lines_file[0][:-1].split(',')
            f.close()
            with open("service.csv", 'r') as csvfile:
                reader = csv.reader(csvfile)
                ser_rows = [row for row in reader]

            single_service = []
            single_service_tweet = []
            for service in services:
                for row in ser_rows:
                    if service == row[0]:
                        single_service += [row[0]]
                        tweet = "{ \"Tweet Type\" : \"Service call\",\"Thing ID\" : \"" + row[1] + "\",\"Space ID\" : \"Group17-VSS\",\"Service Name\" : \"" + row[0] + "\",\"Service Inputs\" : \"()\" }"
                        single_service_tweet += [tweet]
                        break
        
            content = ''
            for i in range(len(single_service)):
                content += single_service[i] + ',' + single_service_tweet[i] + '\n'

            file = open(full_path, 'w')
     
            file.write(content)
            file.close()
           
            currentpath = os.getcwd()
          
            img = Image.open('./image/RGG.png').copy()
            img.save('./image/' + filename[1] + '.png')
            with open('./App.csv', mode='a',newline='') as cfa:
                wf = csv.writer(cfa)
                data = [[filename[1], full_path, currentpath + '\image\\' + filename[1] + '.png']]
                for i in data:
                    wf.writerow(i)
            with open('./Status.csv', mode='a',newline='') as sta:
                wf = csv.writer(sta)
                data = [[filename[1], 'inactive', '', '']]
                for i in data:
                    wf.writerow(i)
        act = Toplevel()
        act.title("activate")
        act.geometry('400x300')

        csv_file = open('./App.csv') 
        csv_reader_lines = csv.reader(csv_file)  
        data = [] 
        for one_line in islice(csv_reader_lines, 1, None):
            data.append(one_line[0])
        actlist = Listbox(act, width = 50)
        for item in data:
            actlist.insert("end", item)
        actlist.pack()
        csv_file.close()

        def Run():
            active_service = []
            index = actlist.get(actlist.curselection())
            run_file = open('./App.csv')
            comparefile = csv.reader(run_file)
            for name in islice(comparefile, 1, None):
                if name[0] == index:
                    path = name[1]
                    print(path)
                    break
            run_file.close()
            
            for line in open(path, 'r'):
                active_service += [line.split(',')[0]]
            df = pd.read_csv('./Status.csv')
            df.loc[df['AppName'] == index, 'Status'] = 'active'
            df.loc[df['AppName'] == index, 'Date'] = time.strftime('%Y-%m-%d')
            df.loc[df['AppName'] == index, 'Time'] = time.strftime('%H:%M:%S')
            df.to_csv('./Status.csv', index=False)
            self.manual = 0
            for service in active_service:
                if self.flag == 1:
                    self.send_tweet(service)
                    appname_log[index].append(str(service) + " is running")  
                    time.sleep(20)
                    self.manual = 2
                else:
                    df1 = pd.read_csv('./Status.csv')
                    df1.loc[df1['AppName'] == index, 'Status'] = 'inactive'
                    df1.loc[df1['AppName'] == index, 'Stop'] = time.strftime('%H:%M:%S')
                    df1.to_csv('./Status.csv', index=False)
                    self.flag = 1
                    self.manual = 1
                    break
            appname_log[index].append(str(index) + " has stopped")
            if self.manual == 2:
                df2 = pd.read_csv('./Status.csv')
                df2.loc[df2['AppName'] == index, 'Status'] = 'Completed'
                df2.loc[df2['AppName'] == index, 'Stop'] = time.strftime('%H:%M:%S')
                df2.to_csv('./Status.csv', index=False)
        Button(act, text="Run!", command= lambda: threading.Thread(target=Run).start()).pack()

    def Status(self):
        status = Toplevel()
        status.title("status")
        status.geometry('600x400')

        def process():
            statu_file = open('./Status.csv') 
            sfile = csv.reader(statu_file) 
            cnt = 1

            def log(s, n):
                if s != "active":
                    pass
                else:
                    def show_msg(count=None):
                        if count is not None:
                            if count <= 1000:
                                txt = str(appname_log[n][-1]) + "\n"
                                textw.insert('end', txt)
                                count += 1
                                top2.after(5432, lambda: show_msg(count))
                        else:
                            show_msg(1)

                    top2 = Toplevel(status)
                    textw = scrolledtext.ScrolledText(top2, width=40, height=25)
                    textw.grid(column=0, row=1, sticky='nsew')
                    textw.config(background='light grey', foreground='black', font='arial 20 bold', wrap='word',
                                 relief='sunken', bd=5)
                    top2.after(1, lambda: show_msg())
                    top2.focus_set()
                    top2.grab_set()

            for rows in islice(sfile, 1, None):
                if rows[1] == 'active':
                    Button(status, text=rows[0], command=lambda: log(rows[1], rows[0])).place(x=30, y=cnt * 50)
                    Label(status, text='status: ' + rows[1]).place(x=120, y=cnt * 50)
                    Label(status, text='start time: ' + rows[2] + ' ' + rows[3]).place(x=220, y=cnt * 50)
                    cnt = cnt + 1
                elif rows[4] != '':
                    current1 = time.strftime('%H:%M:%S')
                    current2 = datetime.datetime.strptime(current1, '%H:%M:%S')
                    print(current2)
                    stopt = datetime.datetime.strptime(rows[4], '%H:%M:%S')
                    delta = current2 - stopt
                    print(delta.seconds)
                    if delta.seconds >= 0 and delta.seconds < 300:
                        Button(status, text = rows[0], command = lambda: log(rows[1], rows[0])).place(x = 30, y = cnt*50)
                        Label(status, text = 'status: ' + rows[1]).place(x = 120, y = cnt*50)
                        Label(status, text='start time: ' + rows[2] +' ' + rows[3]).place(x=220, y=cnt * 50)
                        cnt = cnt + 1
                    else:
                        Button(status, text = rows[0], command = lambda: log(rows[1], rows[0])).place(x = 30, y = cnt*50)
                        Label(status, text='status: removed').place(x=120, y=cnt * 50)
            statu_file.close()

            def Stop():
                stop = Toplevel()
                stop.title("Stop")
                stop.geometry('400x300')

                csv_file = open('./Status.csv')  
                csv_reader_lines = csv.reader(csv_file)
                data = [] 
                for one_line in islice(csv_reader_lines, 1, None):
                    if one_line[1] == 'active':
                        data.append(one_line[0])
                stoplist = Listbox(stop, width=50)
                for item in data:
                    stoplist.insert("end", item)
                stoplist.pack()
                csv_file.close()

                def Ok():
                    index = stoplist.get(stoplist.curselection())  
                    self.flag = 0
                    df = pd.read_csv('./Status.csv')
                    df.loc[df['AppName'] == index, 'Status'] = 'inactive'
                    df.loc[df['AppName'] == index, 'Stop'] = time.strftime('%H:%M:%S')
                    df.to_csv('./Status.csv', index=False)
                Button(stop, text="Ok!", command=lambda: Ok()).pack()

            Button(status, text="Stop", command=lambda: Stop()).place(x = 285, y = 10)
            status.after(20000,process)
        process()

    def send_tweet(self, serviceid):
        with open("service.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            ser_rows = [row for row in reader]
            
        
        for row in ser_rows:
            if row[0] == serviceid:
                tweet = "{ \"Tweet Type\" : \"Service call\",\"Thing ID\" : \"" + row[1] + "\",\"Space ID\" : \"Group17-VSS\",\"Service Name\" : \"" + row[0] + "\",\"Service Inputs\" : \"()\" }"
                thingid = row[1]
                break
        
        with open("thing.csv", 'r') as csvfile:
            reader = csv.reader(csvfile)
            thing_rows = [row for row in reader]
        

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        #thing IP
        sock.connect(('192.168.102.139', 6668))
        sock.send(tweet.encode())
        sock.close()


def back():
    root.destroy()
    os.system("python App.py")

root = Application()
root.geometry('400x300')
root.protocol("WM_DELETE_WINDOW", back)
root.mainloop()