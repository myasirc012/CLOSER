# -*- coding: utf-8 -*-
"""
Created on Fri Jul 22 15:01:20 2022

@author: myc
"""

import requests
import json
import datetime

cpuserial = "0000000000000000"
try:
    f = open('/proc/cpuinfo','r')
    for line in f:
        if line[0:6]=='Serial':
            cpuserial = line[10:26]
    f.close()
except:
    cpuserial = "ERROR000000000"
    
iot_id=cpuserial
secretKey="TIGARD[7Dm5ghNk9HbQYURceIpFLmvviF74kWB0sYiWQbm]"

class create_activity:
    def __init__(self, activity_type1, activity_type2):     
        
        self.date=str(datetime.datetime.now().isoformat())
        self.activity_type1=activity_type1
        self.activity_type2=activity_type2
        self.activity_id=""
        
    def ai_signal_data_create(self, activity_type2, activity_id):
        global iot_id
        global secretKey
        
        url1="https://closerapi03.azurewebsites.net/AiSignalDataCreate"
        
        try:
            payload={'SecretKey': secretKey,
            'IotUniqueId': iot_id,
            'ActivityTypeCode': self.activity_type2,
            'ClientUploadTime': self.date,
            'ActivityId': self.activity_id}
            files=[
                ('FileSta1Phase',(self.activity_type2+"_sta1_phase.npy",open("/home/pi/Desktop/ai_signal_create_test/data/"+self.activity_type2+"_sta1_phase.npy",'rb'),'application/octet-stream')),
                ('FileSta1Amp',(self.activity_type2+"_sta1_amp.npy",open("/home/pi/Desktop/ai_signal_create_test/data/"+self.activity_type2+"_sta1_amp.npy",'rb'),'application/octet-stream')),
                ('FileSta2Phase',(self.activity_type2+"_sta2_phase.npy",open("/home/pi/Desktop/ai_signal_create_test/data/"+self.activity_type2+"_sta2_phase.npy",'rb'),'application/octet-stream')),
                ('FileSta2Amp',(self.activity_type2+"_sta2_amp.npy",open("/home/pi/Desktop/ai_signal_create_test/data/"+self.activity_type2+"_sta2_amp.npy",'rb'),'application/octet-stream'))
            ]
            headers = {
            }
            
            response = requests.request("POST", url1, headers=headers, data=payload, files=files)
            
            res=response.json()
            print("result_AiSignalDataCreate:", res["result"]["success"])
        
        except requests.exceptions.HTTPError as errh:
            print ("Error Connecting:",errh)
            f = open("logs/HTTPerror.txt", "a")
            f.write("http error:"+errh+"---"+self.date+"\n")
            f.close()
            
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            f = open("logs/ConnectionError.txt", "a")
            f.write("ConnectionError:"+errc+"---"+self.date+"\n")
            f.close()
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            f = open("logs/TimeoutnError.txt", "a")
            f.write("Timeout:"+errt+"---"+self.date+"\n")
            f.close()
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
            f = open("logs/RequestException.txt", "a")
            f.write("RequestException:"+err+"---"+self.date+"\n")
            f.close()
        except:
            print("an error")
            f = open("logs/NormalException.txt", "a")
            f.write("an error---"+self.date+"\n")
            f.close()
        finally:
            return
        
    def create_activity(self, activity_type1, activity_type2):    
        global iot_id
        global secretKey
        url = "https://closerapi03.azurewebsites.net/ActivityCreate"
        
        try:
            
            payload = json.dumps({
              "iotUniqueId": iot_id,
              "model1activityTypeCode": self.activity_type1,
              "model2activityTypeCode": self.activity_type2,
              "clientActivityTime": self.date,
              "secretKey": secretKey
            })
            headers = {
              'Content-Type': 'application/json',
            }
            
            response = requests.request("POST", url, headers=headers, data=payload)
 
            res=response.json()
            print("result_ActivityCreate:", res["result"]["success"])
            
            self.activity_id=str(res["id"])
            self.ai_signal_data_create(self.activity_type2, self.activity_id)
            
        except requests.exceptions.HTTPError as errh:
            print ("Error Connecting:",errh)
            f = open("logs/HTTPerror.txt", "a")
            f.write("http error:"+errh+"---"+self.date+"\n")
            f.close()
            
        except requests.exceptions.ConnectionError as errc:
            print ("Error Connecting:",errc)
            f = open("logs/ConnectionError.txt", "a")
            f.write("ConnectionError:"+errc+"---"+self.date+"\n")
            f.close()
        except requests.exceptions.Timeout as errt:
            print ("Timeout Error:",errt)
            f = open("logs/TimeoutnError.txt", "a")
            f.write("Timeout:"+errt+"---"+self.date+"\n")
            f.close()
        except requests.exceptions.RequestException as err:
            print ("OOps: Something Else",err)
            f = open("logs/RequestException.txt", "a")
            f.write("RequestException:"+err+"---"+self.date+"\n")
            f.close()
        except:
            print("an error")
            f = open("logs/NormalException.txt", "a")
            f.write("an error---"+self.date+"\n")
            f.close()
        finally:
            return
        
        
    
        
