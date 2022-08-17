#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 13:59:33 2022

@author: myc
"""

import requests
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
url = "https://closerapi03.azurewebsites.net/AiSignalDataCreate"


class ai_signal_data_create:
    def __init__(self, activity_type):
        
        self.activity_type=activity_type
        self.date=str(datetime.datetime.now().isoformat())

    def ai_signal_data_create(self, activity_type):
        global iot_id
        global secretKey
        global url
        
        payload={'SecretKey': secretKey,
        'IotUniqueId': iot_id,
        'ActivityTypeCode': self.activity_type,
        'ClientUploadTime': self.date}
        files=[
            ('FileSta1Phase',(self.activity_type+"_sta1_phase.npy",open("/home/pi/Desktop/ai_signal_create_test/data/"+self.activity_type+"_sta1_phase.npy",'rb'),'application/octet-stream')),
            ('FileSta1Amp',(self.activity_type+"_sta1_amp.npy",open("/home/pi/Desktop/ai_signal_create_test/data/"+self.activity_type+"_sta1_amp.npy",'rb'),'application/octet-stream')),
            ('FileSta2Phase',(self.activity_type+"_sta2_phase.npy",open("/home/pi/Desktop/ai_signal_create_test/data/"+self.activity_type+"_sta2_phase.npy",'rb'),'application/octet-stream')),
            ('FileSta2Amp',(self.activity_type+"_sta2_amp.npy",open("/home/pi/Desktop/ai_signal_create_test/data/"+self.activity_type+"_sta2_amp.npy",'rb'),'application/octet-stream'))
        ]
        headers = {
        }
        
        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        
        res=response.json()
        print("result:", res["result"]["success"])