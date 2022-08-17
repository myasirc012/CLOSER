# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 13:36:52 2022

@author: myc
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 16:18:37 2022

@author: myc
"""

import serial
import datetime
import sys
import traceback
from threading import Thread

import prediction

   
class serial_data():
    def __init__(self, start):
        self.start=start
        self.subcarrier_group=1
        self.sub_carrier_number=64
        
        self.tag="start"
        self.data="start"
        
        self.amplitude_processed_data=[0]*int((self.sub_carrier_number/self.subcarrier_group))
        self.phase_processed_data=[0]*int((self.sub_carrier_number/self.subcarrier_group))
        self.amplitude_processed1_data=[0]*int((self.sub_carrier_number/self.subcarrier_group))
        self.phase_processed1_data=[0]*int((self.sub_carrier_number/self.subcarrier_group))
        
        self.package_counter=0
        self.wanted_package=5 #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        self.first_few=False
       
        self.array=[]
        self.motherarray=[[[None]*64]*10]*self.wanted_package
        self.wanted_package*=10
        self.nparray=[[None]*64]*self.wanted_package
    
        self.use_amplitude=True
        self.use_phase=False
        
        self.a_stop_threads=False
        
        self.make_prediction=False
        self.want_prediction=True
    
        self.date=str(datetime.datetime.now())
        self.date=self.date.replace(" ",",")
        self.date=self.date.replace(":",".")
        
        self.serialPort = serial.Serial(port = "/dev/ttyAMA1", baudrate=115200,
                               bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        self.serialPort2 = serial.Serial(port = "/dev/ttyAMA2", baudrate=115200,
                                bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    
        
    def serial_data(self, start):
        
            while(True):
                    try:
                        if(self.serialPort.in_waiting > 0) and self.start:
                            
                            serialString = self.serialPort.readline()
                            serialString2 = self.serialPort2.readline()
    
                            #get data from serial
                            data=serialString.decode("utf8",errors='replace')
                            data2=serialString2.decode("utf8",errors='replace')
                            #split string  data
                            splitted_data=data.split(":")
                            splitted_data2=data2.split(":")
                            #if this string is our wanted data
                            if not self.want_prediction:
                                print("-------------------------------------------------------------------------------\n\n data,",data)
                                print("\ndata2, ",data2)
                            if len(splitted_data)==4 and len(splitted_data2)==4:
    
    #!!!!!!!!!!!!!!!!!!!!!!!!!! data counter
                                
                                amplitude_only=[0]*64
                                phase_only=[0]*64
                                both=[0]*128
                                amplitude2_only=[0]*64
                                phase2_only=[0]*64
                                both1=[0]*128
                                #amplitude tag
                                tag=splitted_data[0]
                                phase_tag=splitted_data[2]
                                tag2=splitted_data2[0]
                                phase_tag2=splitted_data2[2]
                                
                                #amplitude data
                                d=splitted_data[1]
                                e=splitted_data2[1]
                                
                                #phase data                      
                                phase=splitted_data[3]
                                phase2=splitted_data2[3]
                                # print("phase2 ",phase2)
                                
                                # print("phase data,",phase)
                                # print("len of data",len(splitted_data))
                                
                                if tag=="CSI_DATA,CSI_AMPL" and phase_tag=="CSI_DATA,CSI_PHAS":
                                    amplitude_data=d.split(" ")
                                    phase_data=phase.split(" ")
                                    amplitude_group_sum=0
                                    phase_group_sum=0
                                    for i in range(0, self.sub_carrier_number):                                    
                                        try:
                                            amplitude_group_sum=amplitude_group_sum+float(amplitude_data[i])
                                            
                                        except:
                                            amplitude_group_sum+=0
                                            
                    
                                        try:
                                            phase_group_sum=phase_group_sum+float(phase_data[i])
                                        except:
                                            phase_group_sum+=0
                                            
                                        if (i+1)%self.subcarrier_group==0:
                                            self.amplitude_processed_data[int((i+1)/self.subcarrier_group)-1]=amplitude_group_sum/self.subcarrier_group
                                            self.phase_processed_data[int((i+1)/self.subcarrier_group)-1]=phase_group_sum/self.subcarrier_group
    
                                            amplitude_group_sum=0
                                            phase_group_sum=0
                                
                                if tag2=="CSI_DATA,CSI_AMPL" and phase_tag2=="CSI_DATA,CSI_PHAS":
                                    amplitude2_data=e.split(" ")
                                    phase2_data=phase2.split(" ")
                                   
                                    
                                    group_sum=0
                                    phase_group_sum=0
                                    for i in range(0,self.sub_carrier_number):
                                        try:
                                            group_sum=group_sum+float(amplitude2_data[i])
                                        except:
                                            group_sum+=0
                                            
                                        try:
                                            phase_group_sum=phase_group_sum+float(phase2_data[i])
                                        except:
                                            phase_group_sum+=0
                                        if (i+1)%self.subcarrier_group==0:
                                            self.amplitude_processed1_data[int((i+1)/self.subcarrier_group)-1]=group_sum/self.subcarrier_group
                                            self.phase_processed1_data[int((i+1)/self.subcarrier_group)-1]=phase_group_sum/self.subcarrier_group
    
                                            group_sum=0
                                            phase_group_sum=0
                                    # print("amplitude_processed_data,", self.amplitude_processed_data)
    #!!!!!!!!!!!!!!!                algorithm starts here:
                                if tag=="CSI_DATA,CSI_AMPL" and phase_tag=="CSI_DATA,CSI_PHAS" and self.want_prediction:
                                    self.package_counter+=1#*
                                    sum1=sum2=sum3=sum4=0
                                    #print(len(self.amplitude_processed_data))                                
                                    for i in range(0,self.sub_carrier_number):
                                        sum1+=float(self.amplitude_processed_data[i])
                                        sum2+=float(self.phase_processed_data[i])
                                        sum3+=float(self.amplitude_processed1_data[i])
                                        sum4+=float(self.phase_processed1_data[i])
                                            
                                        amplitude_only[i]=sum1
                                        phase_only[i]=sum2
                                        amplitude2_only[i]=sum3
                                        phase2_only[i]=sum4
                                            
                                        both1=amplitude_only+phase_only
                                        both2=amplitude2_only+phase2_only
                                        both=both1+both2
                                            
                                        # amplitude_only+=amplitude2_only
                                        # phase_only+=phase2_only
                                        
                                        sum1=sum2=sum3=sum4=0
                                            
                                    #print("\namplitude_only, ", amplitude_only)
                                    # print("phase_only, ", phase_only)
                                    # print("both", both)
                                        
                                    if self.package_counter%10==1:
                                        self.array=[]
                                        
                                        
                                    if self.use_phase and self.use_amplitude:
                                        self.array.append(both)
                                    elif self.use_amplitude and not self.use_phase:
                                        self.array.append(amplitude_only)
                                    elif self.use_phase and not self.use_amplitude:
                                        self.array.append(phase_only)
                                    else:
                                        # print("ERROR: Please use either amplitude or phase or both...")
                                        sys.exit("ERROR: Please use either amplitude or phase or both... see: line 67-68")                                
                                        
                                        
                                    if self.package_counter%10==0:
                                        #print(len(self.array))
                                        #print("\narray, ", self.array)
                                        #print("prediction in ",int((self.wanted_package-self.package_counter)/10))
                                        if(self.package_counter<=self.wanted_package):
                                            self.motherarray[int(self.package_counter/10) - 1]=self.array
                                        
                                        if self.first_few:
                                            self.make_prediction=True
                                            #print(len(self.motherarray))
                                            del self.motherarray[0]
                                            #print(len(self.motherarray))
                                            self.motherarray.append(self.array)
                                            #print(len(self.motherarray))
                                            self.package_counter=0
                                            #print("another", int(self.wanted_package/10), "seconds done")
                                            #print("\nmotherarray, ", self.motherarray)
                                        
                                        elif self.package_counter==self.wanted_package:
                                            self.first_few=True
                                            #print("first", int(self.wanted_package/10), "seconds done")
                                            #print("motherarray, ", self.motherarray)
                                        
                                        
        #!!!!!!!!!!!!!!!!!              algorithm  ends here!
        
                                    if self.make_prediction:
                                        
                                        prediction_object=prediction.prediction(self.motherarray)
                                        
                                        myDataLoop_Stream2 = Thread(name = 'myDataLoop_Stream2', target = prediction_object.prediction,
                                                                              daemon = True, args = (self.motherarray,))
                                        myDataLoop_Stream2.start()   
                                        
                                        self.make_prediction=False
                                
                                        
                            #end second if
                        #end first if
                    #end try
                    except:
                        traceback.print_exc()
                        self.serialPort.close()
                        self.serialPort2.close()
                        print("an error occured")
                        break;
                    # finally:
                    #     serialPort.close()
                        
                    if self.a_stop_threads:
                        print("stop")
                        break;
                #end while
        