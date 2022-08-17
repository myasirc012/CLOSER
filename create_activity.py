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
    
url = "https://closerapi03.azurewebsites.net/ActivityCreate"
iot_id=cpuserial
secretKey="TIGARD[7Dm5ghNk9HbQYURceIpFLmvviF74kWB0sYiWQbm]"

class create_activity:
    def __init__(self, activity_type1, activity_type2):     
        
        self.date=str(datetime.datetime.now().isoformat())
        self.activity_type1=activity_type1
        self.activity_type2=activity_type2
    
    def create_activity(self, activity_type1, activity_type2):    
        global iot_id
        global secretKey
        global url
        
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
            print("result:", res["result"]["success"])
            
            
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
        
