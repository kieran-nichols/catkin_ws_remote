#!/usr/bin/env python

import rospy
import os
import sys
import signal
from rospy.numpy_msg import numpy_msg
from tada_ros.msg import MotorDataMsg
from tada_ros.msg import MotorListenMsg
from tada_ros.msg import IMUDataMsg
from tada_ros.msg import EuropaMsg
from bluepy.btle import *
from uuid import*
from std_msgs.msg import *

import time
import threading
import datetime
import struct
import threading
import os
import sys
#import pyfiglet
import socket

UBLOX_SERVICE_UUID = UUID("2456e1b9-26e2-8f83-e744-f34f01e9d701")
FIFO_CHAR_UUID=UUID("2456e1b9-26e2-8f83-e744-f34f01e9d703")
CREDITS_CHAR_UUID=UUID("2456e1b9-26e2-8f83-e744-f34f01e9d704")
command_start=b"\x67\x0d" # start
command_end=b"\x61\x0d" # end
command_battery=b"\x6b\x00\x0d" # check battery level
INT12BIT_MAX = 4096
INT16BIT_MAX = 65536
EUROPA_KEY=u"Euro"
PLOT_BUFFER_MAX=1000

CAL_FZ=1.96
# Fx: 1bit = 1.96N. For example, Fx=150 means Fx=150*1.96=294N

DBG_FLAG=True
REAL_TIME_PROCESS=True


class ConfigError(Exception):
    def __init__(self,msg):
        self.msg=msg
        self.time=time.time()
    def __str__(self):
        return "ConfigError: "+str(self.msg)

class ConnectError(Exception):
    def __init__(self,msg):
        self.msg=msg
        self.time=time.time()
    def __str__(self):
        return "ConnectError: "+str(self.msg)

class LoggingError(Exception):
    def __init__(self,msg):
        self.msg=msg
        self.time=time.time()
    def __str__(self):
        return "LoggingError: "+str(self.msg)


class EuropaBLE(object):
    
    def __init__(self):
        self.isConnect=False
        self.isStream=False
        self.device_addr=None
        self.device_type=None
        self.ble_scan_time=0
        self.raw_data=[]
        self.target_address=None
        self.key=EUROPA_KEY
        self.iface=1
        self.data_logger=None
        self.buffer=[]
        self.msg_count=0
        self.last_msg=[]
        self.mx_buffer=[]
        self.my_buffer=[]
        self.fz_buffer=[]

        #start ros shananigans
        self.europa_sensing = rospy.Publisher('europa_topic', EuropaMsg, queue_size=10)
        rospy.init_node('EuropaBLE_node', anonymous=True)
        self.europa_command = EuropaMsg()
        
        rate = rospy.Rate(100)#100 hz

        
    def set_device_addr(self,device_addr):    #set device address
        self.target_address=device_addr
    def set_iface(self,iface):
        if iface==0:
            self.turn_on_hci(0)
            self.iface=iface
        if iface==1:
            self.turn_off_hci(0)
            self.iface=iface

    def scan_device(self):   # scan device, by name or by addresss, unicode string
        device_list=[]
        if time.time()-self.ble_scan_time>1200:             #scan interval 60
            scanner = Scanner(self.iface)                  # use hci1, external dongle
            print("Scanning")
            self.scan_results = scanner.scan(10.0)
            self.ble_scan_time=time.time()
        device_list=[]
        for dev in self.scan_results:
            flag_add=False
            if not self.target_address==None and self.target_address in dev.addr:
                flag_add=True
            for (adtype, desc, value) in dev.getScanData():
                if "Name" in desc:
                    if flag_add==True: #find name of device with target address
                        name=value         
                    if not self.key==None and self.key in value: # find device with target name
                        flag_add=True
                        name=value
                        break
            if flag_add==True:           
                device_list.append([dev.addr,dev.addrType,dev.rssi])
                print("scan results "+str(name)+" "+str(dev.addr)+" "+str(dev.rssi))
        if device_list==[]:
            return [0,0]                     # no match device
        flag_find=False
        for (addr, addrType, rssi) in device_list:
            if not self.target_address == None and self.target_address in addr:
                flag_find=True
                return [addr.encode('ascii','ignore'), addrType.encode('ascii','ignore')]#both addresses werer encoded here with encode('ascii','ignore')
        if flag_find==False:                # return device with largest rssi
            max_rssi=-100
            closest_device=["",""]
            for (addr, addrType, rssi) in device_list:
                if rssi>max_rssi:
                    max_rssi=rssi
                    closest_device[0]=addr.encode('ascii','ignore')#.encode('ascii','ignore')
                    closest_device[1]=addrType.encode('ascii','ignore')#encode('ascii','ignore')
            return closest_device

    def search_europa(self):
        res1=self.scan_device()
        if not res1[0] == 0:
            self.device_addr=res1[0]
            self.device_type=res1[1]
            print("found europa "+str(self.device_addr)+" "+str(self.device_type))
            return 0
        else:
            self.device_addr=None
            self.device_type=None
            print("No europa found")
            return 1        

    def findSerialPortSrv(self):
    # Find FIFO & Credits characteristics
        try:
            serial_srv=self.dev.getServiceByUUID(UBLOX_SERVICE_UUID)
            chr_list=serial_srv.getCharacteristics()
            for ch in chr_list:
                if FIFO_CHAR_UUID==ch.uuid:     #Found FIFO characteristics"
                    self.FIFOCh=ch
                    ##print("FIFO charcteristics Handle {} UUID {}".format(str(self.FIFOCh.getHandle()), str(self.FIFOCh.uuid)))
                if CREDITS_CHAR_UUID==ch.uuid:  #Found Credits characteristics
                    self.CreditsCh=ch
                    ##print("Credits charcteristics Handle {} UUID {}".format(str(self.CreditsCh.getHandle()), str(self.CreditsCh.uuid)))
        except Exception as e:
            raise(ConfigError("Can't find Serial Port Service: "+str(e)))
	
    def connectDevice(self):
        class NotifyDelegate(DefaultDelegate):             # callback function for handling notification
            def __init__(self,handle):
                DefaultDelegate.__init__(self)
                self.device_handle=handle                  # EuropaBLE object, for accessing file or lcm
                self.msg_count=0
                self.last_msg=[]
                self.buffer=[]
            def handleNotification(self,cHandle,data):
                #list_data=map(ord,data)
                list_data=data
                for x in list_data:
                    self.device_handle.buffer.append(x)
                if len(self.device_handle.buffer)>3000:
                    self.device_handle.buffer=self.device_handle.buffer[1100:]
                    ##print("drop")
                self.msg_count=self.msg_count+1
                #if self.msg_count % 50 ==0:
                #    #print(self.msg_count)
        
        try:
            self.dev=Peripheral(self.device_addr.decode('utf-8'),iface=self.iface).withDelegate(NotifyDelegate(self))   # hci1, external dongle
            print("[EuropaBLE/connectDevice]"+str(time.time())+" Europa Connected")
        except Exception as e:
            print("[EuropaBLE/connectDevice]Can't connect to device: "+str(e))
            raise(ConnectError(str(e)))


    def turnOnNotify(self,cHandle):
        try:
            value1=self.dev.readCharacteristic(cHandle)
            self.dev.writeCharacteristic(cHandle, struct.pack('<bb', 0x01, 0x00) ,withResponse=True)
            value2=self.dev.readCharacteristic(cHandle)
        except Exception as e:
            raise(ConfigError("Error in turn on Notify"))

    def create_log_file(self,file_path):
        if not file_path==None:
            self.data_logger=open(os.path.join(file_path,"europa_data-"+str(datetime.datetime.now())+".txt"),"wt")
        else:
            self.data_logger=None

    def close_log_file(self):
        if not self.data_logger==None:
            self.data_logger.close()

    def connect(self):
        #if self.device_addr==None:
        #   raise ConnectError("No device address")
        self.isConnect=False
        ##print("[EuropaBLE/connect] Connecting")

        count=3
        while (count>0):
            try:
                self.connectDevice()
                ##print("got stuck 1 in open")
                self.findSerialPortSrv()
                ##print("got stuck 2 in open")
                ##print('Turn on first notification')
                self.turnOnNotify(self.FIFOCh.getHandle()+1)
                ##print("got stuck 3 in open")
                ##print('Turn on second notification')
                self.turnOnNotify(self.CreditsCh.getHandle()+1)
                self.isConnect=True
                count=0
                ##print("[EuropaBLE/connect] Europa configure finished")
                ##print('---------------------Europa Ready------------------------\n')
            except Exception as e:
                #print("[EuropaBLE/connect]Connect failed: "+str(e))
                #print("Try times left "+str(count))
                try:
                    self.dev.disconnect()
                except:
                    pass
                count=count-1
            time.sleep(1)
            
    def disconnect(self):
        try:
            ##printt('[EuropaBLE/disconnect]Europa disconnected')
            self.dev.disconnect()
            self.isConnect=False
        except Exception as e:
            pass
            ##print("[EuropaBLE/disconnect]Error in disconnect Europa:",e)
        finally:
            pass

    def check_connect(self):  #Not working due to bluepy bug
        res=self.dev.getState()
        ##print("checkConnect--------------------------------------------",res)
        if res=='conn':
            self.isConnect=True
        elif res=='disc':
            self.isConnect=False

    def resetBluetooth(self):
        try:
            os.system("rfkill block bluetooth")
            time.sleep(5)
        except:
            pass
        try:
            os.system("rfkill unblock bluetooth")        
        except:
            pass
        time.sleep(2)
        
        
    def turn_off_hci(self,iface):
        try:
            os.system("sudo hciconfig hci"+str(iface)+" down")
        except:
            pass
            ##print("Fail to turn off hci0")
  
        time.sleep(1)
    def turn_on_hci(self,iface):
        try:
            os.system("sudo hciconfig hci"+str(iface)+" up")
        except:
            pass
            ##print("Fail to turn off hci0")
  
        time.sleep(1)


    def stream(self):
        try:
            while self.isStream==True:
                self.dev.waitForNotifications(0.2)
        except Exception as e:
            #print("[EuropaBLE/stream]Error in streaming thread: ",str(e))
            time.sleep(2)
            #raise(LoggingError(str(e),time.time()))
            self.isStream=False
            self.isConnect=False
            self.disconnect()

            
    def start_stream(self):
        
        if self.isConnect==True:
            self.isStream=True
            self.buffer=[]
            self.msg_count=0
            try:
                self.thread=threading.Thread(target=self.stream)
                self.thread.name="stream handler"
                self.thread.setDaemon(True)
                # need the below print statement
                print(self.dev.writeCharacteristic(self.FIFOCh.getHandle(), command_start,withResponse=True))
                #print("[EuropaBLE/start_stream]",str(time.time())," Europa start streaming...")
                self.thread.start()
            except Exception as e:
                pass
                #print("[EuropaBLE/start_stream]Fail to write start command: "+ str(e))
 
    def thread_process_data(self):
        try:
            self.msg_count=0
            while self.isConnect==True and self.isStream==True:
                time.sleep(0.1)   
                # ~ print(self.buffer)             
                while len(self.buffer)>13: 
                    while not self.check_opener(self.buffer) and len(self.buffer)>1:
                        self.buffer=self.buffer[1:]
                    if self.check_opener(self.buffer) and len(self.buffer)>13:
                        msg=self.buffer[0:11]
                        if self.buffer[11]==254 and self.buffer[12]==254:
                            self.buffer=self.buffer[11:]
                        else:
                            self.buffer=self.buffer[8:]
                            continue

                        self.last_msg=self.convert_data(msg)
                        if self.last_msg==None:
                            pass
                            #print("None!!")
                        self.msg_count=self.msg_count+1
                        self.mx_buffer.append(float(self.last_msg[0]))
                        self.my_buffer.append(float(self.last_msg[1]))
                        self.fz_buffer.append(float(self.last_msg[2])*CAL_FZ)
                        
                        #publishing
                        #I think r is the pressure
                        #r is fz_buffer
                        self.europa_command.mx = float(self.last_msg[0])
                        self.europa_command.my = float(self.last_msg[1])
                        self.europa_command.fz = float(self.last_msg[2])*CAL_FZ
                        self.europa_sensing.publish(self.europa_command)
                        
                        t=self.last_msg[2]
                        #if (t>500 or t<-500):
                        #    #print(msg)
                        if self.msg_count>PLOT_BUFFER_MAX:
                            self.mx_buffer=self.mx_buffer[1:]
                            self.my_buffer=self.my_buffer[1:]
                            self.fz_buffer=self.fz_buffer[1:]
                        ##print("self.fz_buffer: ")
                        ##print(type(self.fz_buffer))
                        ##print(self.fz_buffer)
                            
                        if not self.data_logger==None:
                            self.data_logger.write(str(time.time())+str(self.last_msg)+"\n")
                        #if self.msg_count % 100 ==0 and DBG_FLAG:
                            # ~ if len(self.last_msg)==6:
                                # ~ print("F",msg)
                        # ~ #         #print("Mx: %3d, My: %3d, Fz: %3d, Ax: %4d, Ay: %4d, Az: %4d" %  (self.last_msg[0],self.last_msg[1],self.last_msg[2],self.last_msg[3],self.last_msg[4],self.last_msg[5] ) )
                            # ~ else:
                                # ~ print("None")
                       
        except Exception as e:
            pass
                #print("[EuropaBLE/thread_process_data]",e)
        #print("[EuropaBLE/thread_process_data] thread quit")

    def process_data(self):
        self.process_thread=threading.Thread(target=self.thread_process_data)
        self.process_thread.name="thread_process_data handler"
        self.process_thread.setDaemon(True)
        self.process_thread.start()
        
    def get_fz_data(self):
        return self.fz_buffer
    def get_mx_data(self):
        return self.mx_buffer
    def get_my_data(self):
        return self.my_buffer
        
    def stop_stream(self):
        if self.isStream==True:
            try:
                #print(self.dev.writeCharacteristic(self.FIFOCh.getHandle(), command_end,withResponse=True))
                self.isStream=False
                #self.file.write('Stop streaming\n')
                while self.dev.waitForNotifications(1):
                    pass
                ##print(self.thread.isAlive())
                if self.thread.isAlive():
                    self.thread.join()
                #print('[EuropaBLE/stop_stream]Streaming thread quit, Stop stream')
            except Exception as e:
                pass
                #print("[EuropaBLE/stop_stream]stop stream failed:",str(e))
                
    def check_stream(self):
        pass


    def check_battery(self):      #Not working
        #print("----------------check battery---------------------")
        #print(self.dev.writeCharacteristic(self.FIFOCh.getHandle(), command_battery,withResponse=True))
        self.dev.waitForNotifications(3)  
        self.dev.waitForNotifications(3) 
        self.dev.waitForNotifications(3) 
        
    def check_opener(self,data):
        if len(data)>1:
            if data[0]==254 and data[1]==254:
                return True
        return False
        
    def convert_data(self,data):
        def get_sign(x):
            if x & 2048 > 0:
                return x-4096
            else:
                return x
        if not len(data)==11:
            return None
        pyr_ml=(data[2]<<4)+(data[3]>>4)
        pyr_ml=get_sign(pyr_ml)
        pyr_ap=((data[3]&15) << 8) + data[4]
        pyr_ap=get_sign(pyr_ap)
        pyr_ax=(data[5]<<4)+(data[6]>>4)
        pyr_ax=get_sign(pyr_ax)
        acce_x=((data[6]&15) << 8) + data[7]
        acce_x=get_sign(acce_x)
        acce_y=(data[8]<<4)+(data[9]>>4)
        acce_y=get_sign(acce_y)
        acce_z=((data[9]&15) << 8) + data[10]
        acce_z=get_sign(acce_z)
        return [pyr_ml, pyr_ap,pyr_ax, acce_x, acce_y, acce_z] 
        
    def parse_data(self):   
        flag_time=False
        current_time=0
        stream=[]
        converted_data=[]
        #print("\n\nConvert")
        for data_timestamp,data in self.raw_data:
            for x in map(ord,data):
                stream.append(x)
            while len(stream)>10:
                if not self.check_opener(stream):
                    stream=stream[1:]
                if self.check_opener(stream) and flag_time==False:
                    current_time=data_timestamp
                    flag_time=True
                if self.check_opener(stream) and len(stream)>10:
                    ##print(stream[0:11])
                    converted_data.append(self.convert_data(stream[0:11]) )
                    stream=stream[11:]
                    flag_time=False
                if self.check_opener(stream) and flag_time==False:
                    current_time=data_timestamp
                    flag_time=True
        return converted_data
 





