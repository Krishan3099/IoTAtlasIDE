import tkinter as tk
from tkinter import ttk
import socket
import struct
import queue
import threading
import select

thing_num = 0
thing_ip = []
ss_name = ''
start_flag = 0
num = 1


class InitPage(tk.Frame):
    def __init__(self, parent, controller):

        global thing_num, thing_ip
        tk.Frame.__init__(self, parent)
        self.queue = queue.Queue()

        thing_ip = ''
        l1 = tk.Label(self, text="VSS Name:")
        l1.place(x=10, y=10)
        self.ssname_text = tk.Entry(self, relief=tk.RIDGE) 
        self.ssname_text.place(x=250, y=10)

        l2 = tk.Label(self,
                      text="Number of Things: ")
        l2.place(x=10, y=50)
        self.thingnum_text = tk.Entry(self, width=70, relief=tk.RIDGE)
        self.thingnum_text.place(x=10, y=80)


        self.l4 = tk.Label(self, text="Click Start when info is inputed")
        self.l4.place(x=10, y=120)

        self.pbar = ttk.Progressbar(self, orient='horizontal', length=300, mode='determinate')
        self.btn = tk.Button(self, text="Start", command=lambda: self.spawnthread(controller))

        self.btn.place(x=390, y=150)
        self.pbar.place(x=260, y=180)

    def spawnthread(self, controller):
        global thing_num, num, thing_ip, ss_name, start_flag
        input_appropriate = True
        temp_things = []
        
        ss_name = self.ssname_text.get()      
        thing_num = self.thingnum_text.get()
      
        if ss_name == '' or thing_num == '' or  not ('0' < thing_num[0] <= '9'):
            tk.messagebox.showinfo('Error', 'Input Info Correctly!')
            input_appropriate = False
        else:
            for i in range(1, len(thing_num)):
                if not ('0' <= thing_num[i] <= '9'):
                    tk.messagebox.showinfo('Error', 'Input Info Correctly!')
                    input_appropriate = False
                    break
            
        if input_appropriate == True:
            num = int(thing_num)
            thing_num = int(thing_num)
            print("thing_num:", thing_num)

            self.btn.config(state="disabled")
            self.thread = ThreadedClient(self.queue)
            self.thread.start()
            self.periodiccall()

            self.l4['text'] = "Running! May take a bit."

            from startpage import StartPage
            self.btn['command'] = lambda: controller.show_frame(StartPage)

    def periodiccall(self):

        self.checkqueue()
        if self.thread.is_alive():
            self.after(100, self.periodiccall)
        else:
            self.btn.config(state="active")
            if start_flag == 1:
                self.l4['text'] = "Wrong input, please restart program."
                self.btn["text"] = "Close"
                self.btn["command"] = lambda: InitPage.quit(self)

    def checkqueue(self):
        global num 
        while self.queue.qsize():
            msg = self.queue.get(0)
            self.pbar['value'] += 100 / num
        


class ThreadedClient(threading.Thread):

    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run(self):
        global thing_num, thing_ip, ss_name, start_flag
        global num  
    
        thingID = {}
        ipaddr = {}
        thingIdx = {}
   

        onlineThing = set()
        firstTweet = [''] * thing_num
        serviceInfo = [[]]
        relationshipInfo = [[]]
        count = 0
        for j in range(thing_num - 1):
            serviceInfo += [[]]
            relationshipInfo += [[]]

        print("firstTweet: ", firstTweet)
        print("serviceInfo: ", serviceInfo)
        print("relationshipInfo", relationshipInfo)

        multicast_group = '232.1.1.1'
        server_address = ('', 1235)

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server_address))

        group = socket.inet_aton(multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    

        while True:
            sock.setblocking(0)
            ready = select.select([sock], [], [], 60)
            if ready[0]:
                data, server = sock.recvfrom(4096)     
            else:
                start_flag = 1
                tk.messagebox.showinfo('Error', 'Time out! Close program and try again.')
                break
    
            vss = "\"Space ID\" : \"" + ss_name + "\""
            str1 = data.decode("utf-8")
            print(str1)
            if vss not in str1:
                continue

            datadict = data.decode("utf-8").replace("\"waitingTime_Seconds\"", "waitingTime_Seconds")
        
            datadict = datadict.replace("'", "_")
            datadict = datadict.replace("\"", "'")
        
            datadict = eval(datadict)

            #print
            print(str(datadict))

          
            thing = datadict['Thing ID']
            tweetType = datadict['Tweet Type']
            
            if thing not in thingID and count == thing_num:
                continue

            if datadict in firstTweet:
                print("pop: " + str(thingID))
                thingID.pop(thing)
                print("pop: " + str(thingID))
                self.queue.put(num)
                if not thingID:
                    break
                
            else:
                if thing not in onlineThing and count < thing_num:
                    onlineThing.add(thing)
                    thingID[thing] = count
                    ipaddr[thing] = count
                    firstTweet[count] = datadict
                    print(onlineThing)
                    index = thingID[thing]
                    print("new thing: ", thing, index)
                    print("first:" + str(firstTweet))
                    count += 1
                    print("count: ", count)
                else:
                    index = thingID[thing]
                    print("existed thing, index", thing, index)

                print(thing, index, tweetType)

                if tweetType == "Identity_Language":
                    ipaddr[thing] = datadict['IP']
                    thingIdx[thing] = index
                elif tweetType == 'Service':
                    serviceInfo[index].append(datadict['Name'])
                    print("datadict['Name'] ", datadict['Name'])
                    print("serviceInfo ", serviceInfo)
                elif tweetType == 'Relationship':
                    rs = [datadict['Name'], datadict['Type'], datadict['FS name'], datadict['SS name']]
                    relationshipInfo[index].append(rs)
                    print(relationshipInfo)
        
        sock.close()
        print("")
        print("Reception done!\n")
        print("onlineThing: ", onlineThing)
        print("ipaddr: ", ipaddr)
        print("thingIdx: ", thingIdx)
        print("serviceInfo: ", serviceInfo)
        print("relationshipInfo", relationshipInfo)

       
        onlineThing = list(onlineThing)
        
        f = open('thing.csv', 'w')
        for thingId in ipaddr:
            f.write(thingId + ',' + "192.168.102.139" + '\n')
        f.close()
        dataArray = {"Tweet Type": "Service", "Name": "button_pushed", "Thing ID": "Pi-Varun", "Entity ID": "Pushbutton",
                "Space ID": "Group17-VSS", "Vendor": "", "API": "button_pushed:[NULL]:(buttonState,int, NULL)",
                "Type": "Report", "AppCategory": "Environment Monitor",
                "Description": "Returns 1 if the button is currently being pushed, 0 if not.", "Keywords": ""}
        dataArray1 = { "Tweet Type" : "Identity_Entity","Thing ID" : "Pi-Varun","Space ID" : "Group17-VSS","Name" : "Raspberry Pi internal CPU temperature sensor","ID" : "CPU_TEMP","Type" : "Built-In","Owner" : "","Vendor" : "","Description" : "" }
        dataArray2 = { "Tweet Type" : "Identity_Entity","Thing ID" : "Pi-Varun","Space ID" : "Group17-VSS","Name" : "Red LED","ID" : "LIGHT_RED","Type" : "Connected","Owner" : "","Vendor" : "","Description" : "A red LED connected on GPIO pin 9" }
        dataArray3 = { "Tweet Type" : "Identity_Entity","Thing ID" : "Pi-Varun","Space ID" : "Group17-VSS","Name" : "Green LED ","ID" : "LIGHT_GREEN","Type" : "Connected","Owner" : "","Vendor" : "","Description" : "A green LED connected on GPIO 11" }
        resultdict=[]
        resultdict.append(dataArray)
        resultdict.append(dataArray1)
        resultdict.append(dataArray2)
        resultdict.append(dataArray3)
        serviceInfo = [['cpu_temp', 'button_pushed', 'toggle_green', 'toggle_red'], [], [], [], []]
        f = open('service.csv', 'w')
        for i in range(len(serviceInfo)):
            for j in thingIdx:
                if thingIdx[j] == i:
                    thing = j
                    break
            for service_name in serviceInfo[i]:
                f.write(str(service_name) + ',' + str(thing) + '\n')
        f.close()

        f = open('relationship.csv', 'w')
        f.write("Name,Type,Service1,Service2" + '\n')
        for data in resultdict:
                f.write(
                str(data.get('Name')) + ',' + str(data.get('Type')) + ',' + str(data.get('Entity ID')) + ',' + str(data.get('Entity ID')) + '\n'
            )
        f.close()

