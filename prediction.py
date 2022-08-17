# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:57:33 2022

@author: myc
"""
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler  
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix
from sklearn.linear_model import RidgeClassifierCV
from threading import Thread
import time
import os
# import board
# import adafruit_dht

import create_activity
import iot_ping_create
import ai_signal_data_create

fall_counter=0
walking_counter=0
nobody_counter=0
sitting_counter=0
last_activity=""
last_activity1=""
new_array=[]

motion_counter=0
prediction_counter=0

# temp=0
# hum=0
# temp_hum_count=0
previous_time=time.time()

class prediction:
    
    def __init__(self, motherarray):
        self.motherarray=motherarray
        # self.filename = 'model/cov_updated_KNN_4_slide35.sav'
        # self.filename = 'model/cov_updated_RANDOMfOREST_4_slide35.sav'
        self.filename = '/home/pi/Desktop/CLOSER/model/coef_updated_rf_4.sav'
        self.model = pickle.load(open(self.filename, 'rb'))
        
        self.filename = '/home/pi/Desktop/CLOSER/model/motion_nonmotion_cov_rf_4.sav'
        self.model_motion = pickle.load(open(self.filename, 'rb'))
        
        self.sec=10
        self.ping_time=10
        # self.Error=False
        self.current_time=time.time()
        
        # dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)
        
        # try:
        #     self.temperature_c = dhtDevice.temperature
        #     self.humidity = dhtDevice.humidity           
    
        # except RuntimeError:
        #     self.Error=True
            
        # except Exception as error:
        #     dhtDevice.exit()
        #     raise error
           
    def run_model_coefcorr(self, data,model):
         #data 50X64 array
         #model: given ai model
        sample_number=45
        test_list=[]
        test=data.copy()
        #not all of the subcarriers included
        drops=[0,1,2,3,4,5,59,60,61,62,63]
        test=np.delete(test,drops,1)
        test=test.astype(float)
        
        # print("data shape must be (50,53)")
        # print("data shape is :",test.shape)
        corcmatrix_A=np.corrcoef(test,rowvar=False)
        corcmatrix_A = np.nan_to_num(corcmatrix_A)
        w, v = np.linalg.eig(corcmatrix_A)
        w=w/sample_number
        eigens=np.array([w[0],w[1],w[2],w[3],w[4]])
        test_list.append(eigens)
        # print(test_list)
        test_data=np.array(test_list,dtype=float)
        y_pred=model.predict(test_data)
         
    
        return y_pred
    
    def run_model_coefcorr_motion(self,data,model):
        #data 50X64 array
        #model: given ai model
        sample_number=50
        test_list=[]
        test=data.copy()
        test=test.astype(float)
        corcmatrix_A=np.corrcoef(test)
        w, v = np.linalg.eig(corcmatrix_A)
        w=w/sample_number
        eigens=[w[0],w[1],w[2]]
        test_list.append(eigens)
        print(test_list)
        test_data=np.array(test_list,dtype=float)
        y_pred=model.predict(test_data)
             

             
        #if y_pred == 0 it means nonmotion
        #if y_pred == 1 it means motion
        return y_pred
        
    def run_model_cov(self, data,model):
        #data 50X64 array
        #model: given ai model
        sample_number=45
        test_list=[]
        test=data.copy()
        #not all of the subcarriers included
        drops=[0,1,2,3,4,5,59,60,61,62,63]
        test=np.delete(test,drops,1)
        test=test.astype(float)
        # print("data shape must be (50,53)")
        # print("data shape is :",test.shape)
        covmatrix_A=np.cov(test)
        corcmatrix_A = np.nan_to_num(covmatrix_A)
        w, v = np.linalg.eig(covmatrix_A)
        w=w/sample_number
        eigens=np.array([w[0],w[1],w[2],w[3],w[4]])
        test_list.append(eigens)
        # print(test_list)
        test_data=np.array(test_list,dtype=float)
        y_pred=model.predict(test_data)
     
        return y_pred
    
    def run_model_cov_motion_nonmotion(self, data,model):
        #data 50X64 array
        #model: given ai model
        sample_number=45
        test_list=[]
        test=data.copy()
        #not all of the subcarriers included
        drops=[0,1,2,3,4,5,59,60,61,62,63]
        test=np.delete(test,drops,1)
        test=test.astype(float)
    #    print("data shape must be (50,53)")
    #    print("data shape is :",test.shape)
        covmatrix_A=np.cov(test)
        corcmatrix_A = np.nan_to_num(covmatrix_A)
        w, v = np.linalg.eig(covmatrix_A)
        w=w/sample_number
        eigens=np.array([w[0],w[1],w[2],w[3],w[4]])
        test_list.append(eigens)
        #print(test_list)
        test_data=np.array(test_list,dtype=float)
        y_pred=model.predict(test_data)
     
        return y_pred
     
    def prediction(self,motherarray):
        global motion_counter
        global prediction_counter
        global fall_counter
        global walking_counter
        global nobody_counter
        global sitting_counter
        global last_activity
        global last_activity1
        global new_array
        # global temp
        # global hum
        # global temp_hum_count
        global previous_time
        
        current_time=time.time()
        
        nparray=np.asarray(self.motherarray)
        nparray = nparray.reshape(nparray.shape[0] * nparray.shape[1], nparray.shape[2])
        
        prediction=self.run_model_coefcorr(nparray,self.model)
        motion_prediction=self.run_model_cov_motion_nonmotion(nparray,self.model_motion)
        prediction_counter+=1
        
        if motion_prediction==0:
            print("----class nonmotion----")         
        elif motion_prediction==1:
            print("----class motion----")
            motion_counter+=1
        
        if prediction==0:
            print("----class fall----")
            fall_counter+=1
            
        elif prediction==1:
            print("----class walking----")
            walking_counter+=1
        
        elif prediction==2:
            print("----class nobody----")
            nobody_counter+=1
            
        elif prediction==3:
            print("----class sitting----")
            sitting_counter+=1
        
        # if not self.Error:
        #     temp+=self.temperature_c
        #     hum+=self.humidity
        #     temp_hum_count+=1    
        
        if prediction_counter%5==0:
            new_array+=self.motherarray
            
        if prediction_counter==self.sec:
            motion_rate=motion_counter/prediction_counter*100
            print("\n\nmotion rate in the last " + str(self.sec) +  " seconds: %" + str(motion_rate))
            activity1 ="motion" if  motion_rate >=50 else "nonmotion"
            
            
            print("fall_counter:",fall_counter)
            print("walking_counter:",walking_counter)
            print("nobody_counter:",nobody_counter)
            print("sitting_counter:",sitting_counter)
            
            if fall_counter/self.sec>0.5 or walking_counter/self.sec>0.5 or nobody_counter/self.sec>0.5 or sitting_counter/self.sec>0.5:
                var = {fall_counter:"fall",walking_counter:"walking",nobody_counter:"nobody", sitting_counter:"sitting"}
                activity=var.get(max(var))
            else:
                activity="unsure"
                
            print("\n\n" + activity1)
            print(activity)
           
            
            prediction_counter=0
            fall_counter=0
            walking_counter=0
            nobody_counter=0
            sitting_counter=0
            motion_counter=0
        
            m = int(time.strftime("%M", time.localtime())) 

            if not activity1==last_activity1 or not activity==last_activity or m < 1: 
                create_activity_object=create_activity.create_activity(activity1,activity)
                myDataLoop_Stream3 = Thread(name = 'myDataLoop_Stream3', target = create_activity_object.create_activity,
                                                      daemon = True, args = (activity1,activity,))
                myDataLoop_Stream3.start()
                
                
                narray=np.asarray(new_array)
                narray = narray.reshape(narray.shape[0] * narray.shape[1], narray.shape[2])
                
                np.save("/home/pi/Desktop/ai_signal_create_test/data/"+activity+"_sta1_phase.npy", narray, allow_pickle=True, fix_imports=True)
                np.save("/home/pi/Desktop/ai_signal_create_test/data/"+activity+"_sta1_amp.npy", narray, allow_pickle=True, fix_imports=True)
                np.save("/home/pi/Desktop/ai_signal_create_test/data/"+activity+"_sta2_phase.npy", narray, allow_pickle=True, fix_imports=True)
                np.save("/home/pi/Desktop/ai_signal_create_test/data/"+activity+"_sta2_amp.npy", narray, allow_pickle=True, fix_imports=True)
                
                ai_signal_data_create_object=ai_signal_data_create.ai_signal_data_create(activity)
                myDataLoop_Stream4 = Thread(name = 'myDataLoop_Stream4', target = ai_signal_data_create_object.ai_signal_data_create,
                                                      daemon = True, args = (activity,))
                myDataLoop_Stream4.start()
                
                
                last_activity1=activity1
                last_activity=activity
            new_array=[]
            narray=[]
            
        if current_time-previous_time>=self.ping_time:
            previous_time=current_time
            
            average_temp = 25 #temp/temp_hum_count
            average_hum = 25 # hum/temp_hum_count
#             temp=0
#             hum=0
#             temp_hum_count=0
            
            print("average temp: " + str(average_temp) + "average hum: " + str(average_hum))
            
            iot_ping_create_object=iot_ping_create.iot_ping_create(average_temp,average_hum)
            
            myDataLoop_Stream5 = Thread(name = 'myDataLoop_Stream5', target = iot_ping_create_object.iot_ping_create,
                                                          daemon = True, args = (average_temp,average_hum,))
            myDataLoop_Stream5.start()
            #myDataLoop_Stream5.join()
