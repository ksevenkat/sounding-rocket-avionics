from posixpath import isabs
from tkinter import * 
from tkinter import ttk
from random import randint
from matplotlib.cbook import index_of
from pyparsing import col
import serial,serial.tools.list_ports
import sys,os, time
from turtle import bgcolor, width
from PIL import ImageTk,Image  
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import filedialog
import paho.mqtt.client as mqtt
import matplotlib.animation as animation
from matplotlib import style
import threading
import random
import pandas as pd


style.use("ggplot")


ONCMD = 'ON'
OFFCMD = 'OFF'









def find_USB_device(USB_DEV_NAME=None):
    myports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
    print(myports)
    usb_port_list = [p[0] for p in myports]
    usb_device_list = [p[1] for p in myports]
    print(usb_device_list)

    if USB_DEV_NAME is None:
        return myports
    else:
        USB_DEV_NAME=str(USB_DEV_NAME).replace("'","").replace("b","")
        for device in usb_device_list:
            print("{} -> {}".format(USB_DEV_NAME,device))
            print(USB_DEV_NAME in device)
            if USB_DEV_NAME in device:
                print(device)
                usb_id = device[device.index("COM"):device.index("COM")+4]
            
                print("{} port is {}".format(USB_DEV_NAME,usb_id))
                return usb_id


class handleDataFrame():
        def __init__(self):
                self.fileNameForLogs = "log.csv"
                self.info = [0,0,0]
                self.altitude = [0,0,0,0,0,0,0,0,0,0]
                self.temperature = [0,0,0,0,0,0,0,0,0,0]
                self.pressure = [0,0,0,0,0,0,0,0,0,0]
                self.finalList = []

        def saveData(self, dataList):
                try:
                        self.info[0] = dataList[0]
                        self.info[1] = dataList[1]
                        self.info[2] = dataList[2]

                        # update gyro and gps 
                        # main.gyroX = dataList[3]
                        logFile = pd.read_csv(self.fileNameForLogs)
                        logFile.loc[len(logFile)] = dataList
                        self.plotGraphs()
                except:
                        pass
                finally:
                        main.serial.flush()
                        
        def plotGraphs(self):
                lis=['Altitude','Temperature','Pressure']
                self.finalList = [self.altitude,self.temperature,self.pressure]
                
                print(self.finalList)
                for i in range(3):
                        self.finalList[i].append(self.info[i])
                        if(len(self.finalList[i])>10):
                                self.finalList[i].pop(0)
                j=0
                for rows in main.a:
                        for cols in rows:
                                if len(self.finalList[j])==10:
                                        cols.clear()
                                        cols.set_xlabel('time')
                                        cols.xaxis.label.set_color("whtie")
                                        cols.set_ylabel(lis[j])
                                        cols.yaxis.label.set_color("white")
                                        cols.plot([1,2,3,4,5,6,7,8,9,10],self.finalList[j])
                                else:
                                        cols.clear()
                                        cols.set_xlabel("time")
                                        cols.xaxis.label.set_color("white")
                                        cols.set_ylabel(lis[j])
                                        cols.yaxis.label.set_color("white")
                                        cols.plot([1,2,3,4,5,6,7,8,9,10],[0,0,0,0,0,0,0,0,0,0])
                                j = j+1
                main.canvas.draw()
                





class Mainwindow(object):
  

        def sendData(self, commandSend):
                if self.serial is None:
                        print('serial port not open')
                else:
                        if commandSend != "":
                                ## CONTAINER GCS
                                # commandSend = commandSend + "\n"

                                ## PAYLOAD GCS
                                commandSend = commandSend
                                print('sending->')
                                print(commandSend)
                                self.serial.write(bytearray(commandSend.encode()))
                                #answer=self.readData()
                                #self.desc.setText(answer)
                                #self.desc.setText(self.desc.toPlainText()+"\n"+answer)
                        time.sleep(0.5);         
                        # recv = self.readData()
                        # print(recv)
                        # self.desc.setText(recv)


        def _readUpdate(self):
                if self.serial is None:
                        print("no connection")
                else:
                        # self.serial.open()
                        while(self.dataIn):
                                print("reading data")
                                recv = self.readData()
                                self.serial.flush()
                                print(recv)
                                dfsaveplot.saveData(recv.split(','))
                                
                                time.sleep(1)
                                
                        # self.serial.close()
        def readData(self):
                answer=""
                while  self.serial.inWaiting()>0:
                        answer += str(self.serial.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
                return answer 
                
        def _scan(self):

                self.portlist['values'] = find_USB_device()
                print('working')

        def _stop(self):

                if self.serial is None: 
                        print("no connection")
                else: 
                        self.serial.close()
                        self.serial = None

                # dfsaveplot.plotGraphs()
                print('working')

        def _start(self):
                
                portToConnect = (self.portlist["values"][int(self.portlist.current())][0])
                if self.serial is None:
                        self.serial = serial.Serial()
                        self.serial.baudrate = 9600
                        self.serial.port = portToConnect
                        self.serial.open()
                else:
                        print("Already Opened")
                print('working')

                print(self.value)
        
        def _on(self):
                self.dataIn = True
                # self.serial.open()
                self.sendData(ONCMD)
                time.sleep(0.5)
                t1 = threading.Thread(target=self._readUpdate)
                t1.start()
                print('working')
        def _off(self):
                self.dataIn = False
                self.sendData(OFFCMD)
                print('working')



        def __init__(self,root):
                self.value=0
                # self.softwareStateVal = "IDLE"
                self.gyroX = 0
                self.gyroy = 0
                self.gyroz = 0
                self.gpslat = 0
                self.gpslong = 0
                self.gpstime = '12:12:12'
                self.dataIn = False
                self.isActviated = False
                self.serial = None        
                self.im1 = ImageTk.PhotoImage(Image.open("Capture1.png"))
        
                self.topframe=Frame(root,height=100, relief=SUNKEN, bg='white')
                self.topframe.pack(fill=BOTH)
                # self.label1=Label(self.topframe,image=self.im2,bg='white')
                # self.label1.grid(row=0,column=0,padx=10,ipadx=20)
                self.label2=Label(self.topframe,image=self.im1,bg='white')
                self.label2.grid(row=0,column=1,padx=20,ipadx=20, sticky="e")
                # self.label3=Label(self.topframe,image=self.im3,bg='white')
                # self.label3.grid(row=0,column=2,padx=10,ipadx=20)
                self.topframe2=Frame(root,height=100, relief=SUNKEN, bg='black')
                self.topframe2.pack(fill=BOTH)
                # self.label4=Label(self.topframe2,image=self.im4,bg='black')
                # self.label4.grid(row=0,column=0,padx=10,ipadx=20)
                self.innerframe=Frame(self.topframe2,relief=SUNKEN, bg='black',bd=2)
                self.innerframe.grid(row=0,column=1,padx=10,ipadx=20)
                self.label5=Label(self.innerframe,text='PORT',bg='black',fg='white')
                self.label5.grid(row=0,column=0,padx=10,ipadx=20)
                self.label6=Label(self.innerframe,text='BAUDRATE',bg='black',fg='white')
                self.label6.grid(row=0,column=1,padx=10,ipadx=20)
                self.innerframe2=Frame(self.topframe2,relief=SUNKEN, bg='black',bd=2)
                self.innerframe2.grid(row=0,column=2,padx=10,ipadx=20)


                #telemetry on and off

                self.innerframe3=Frame(self.topframe2,relief=SUNKEN, bg='black',bd=2)
                self.innerframe3.grid(row=0,column=3,padx=10,ipadx=20)
              
                self.label7=Label(self.innerframe3,text='TELEMETRY',bg='black',fg='white')
                self.label7.grid(row=0,column=0,ipadx=20)
                self.label8=Frame(self.topframe2,relief=SUNKEN,bg='black',bd=2)
                self.label8.grid(row=0,column=4,padx=10,ipadx=20)
                self.label23 = Label(self.label8, text="GYRO DATA",bg = 'black',fg = "white")
                self.label23.grid(row=0,column=1,ipadx=20)
                self.label24 = Label(self.label8, text="X : "+str(self.gyroX), bg= 'black', fg='white')
                self.label24.grid(row=1,column=0,ipadx=20)
                self.label25 = Label(self.label8, text="Y : "+str(self.gyroy), bg= 'black', fg='white')
                self.label25.grid(row=1,column=1,ipadx=20)
                self.label26 = Label(self.label8, text="Z : "+str(self.gyroz), bg= 'black', fg='white')
                self.label26.grid(row=1,column=2,ipadx=20)
                self.label27 = Frame(self.topframe2,relief=SUNKEN, bg="black", bd = 2)
                self.label27.grid(row=0,column=5,padx=10,ipadx=20)
                self.label30 = Label(self.label27, text="GPS DATA", bg='black',fg='white')
                self.label30.grid(row=0,column=1,ipadx=20)
                self.label30 = Label(self.label27, text="GPS LAT: "+str(self.gpslat), bg='black',fg='white')
                self.label30.grid(row=1,column=0,ipadx=20)
                self.label30 = Label(self.label27, text="GPS LONG: "+str(self.gpslong), bg='black',fg='white')
                self.label30.grid(row=1,column=1,ipadx=20)
                self.label30 = Label(self.label27, text="GPS TIME: "+str(self.gpstime), bg='black',fg='white')
                self.label30.grid(row=1,column=2,ipadx=20)

                # self.valueOfData = Label(self.label8,text=self.softwareStateVal,bg='black', fg='white')
                # self.valueOfData.grid(row=1,column=0,ipadx=20)

                #telemtry on and off buttons
                self.telemetry_on=Button(self.innerframe3,text='ON',bg='black',fg='white',command=self._on)
                self.telemetry_on.grid(row=2,column=0,padx=10,ipadx=20, pady=5)
                self.telemetry_off=Button(self.innerframe3,text='OFF',bg='black',fg='white',command=self._off)
                self.telemetry_off.grid(row=2,column=1,padx=10,ipadx=20, pady=5)
                #port combo box
                self.port = StringVar()
                self.portlist = ttk.Combobox(self.innerframe,textvariable = self.port,width=10) #port combo box
        
        # Adding port drop down list
                self.portlist['values'] = find_USB_device()
                self.portlist.grid(row=2,column=0,padx=10,ipadx=20)
                self.portlist.current()
                self.baudrate = StringVar()
                self.baudratelist = ttk.Combobox(self.innerframe,textvariable = self.baudrate,width=10) #port combo box
        
        # Adding buadrate top down list
                self.baudratelist['values'] = ('9600')
                self.baudratelist.grid(row=2,column=1,padx=10,ipadx=20)
                self.baudratelist.current()

        #scan stop buttons gui
                self.scan=Button(self.innerframe,text='SCAN',bg='white',fg='black',command=self._scan)
                self.scan.grid(row=3,column=0,padx=10,ipadx=20,pady=5)
                self.start=Button(self.innerframe,text='CONNECT',bg='white',fg='black',command=self._start)
                self.start.grid(row=3,column=2,padx=10,ipadx=20,pady=5)
                self.stop=Button(self.innerframe,text='STOP',bg='white',fg='black',command=self._stop)
                self.stop.grid(row=3,column=1,padx=10,ipadx=20,pady=5)


        #tabbed window
                self.graphwindow=Frame(root,bg='black')
        
                self.graphwindow.pack(side=LEFT,fill=BOTH,expand=1)
                self.payload_telemetry=Frame(self.graphwindow,bg='black')
                self.payload_telemetry.pack(fill=BOTH,expand=1)
                f,self.a =plt.subplots(nrows=1, ncols=3,figsize=(10,5))
                f.tight_layout()
                f.patch.set_facecolor('black')
                
                
                print(self.a)
                self.canvas = FigureCanvasTkAgg(f, self.payload_telemetry)
                
                self.canvas.get_tk_widget().pack(fill=BOTH,expand=1)
                self.canvas.get_tk_widget().configure()
                

                self.canvas._tkcanvas.pack(fill=BOTH,expand=1)
                
        

 

        

root=Tk()
root['background']='white'
width= root.winfo_screenwidth()               
height= root.winfo_screenheight()               
root.geometry("%dx%d" % (width, height))
# root.attributes('-fullscreen', True)
# root.configure(background='black')

main=Mainwindow(root)
dfsaveplot = handleDataFrame()
# mqt=mq(main)
root.mainloop()
