#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 26 17:29:30 2022

@author: pi
"""

import requests
import socket
import json
import fcntl
import struct
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
    
ifname='eth0'
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_ip=socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
except:
    ifname='wlan0'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    local_ip=socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])
    
public_ip = requests.get('https://api.ipify.org').text
iot_id=cpuserial
secretKey="TIGARD[7Dm5ghNk9HbQYURceIpFLmvviF74kWB0sYiWQbm]"
url = "https://closerapi03.azurewebsites.net/IotPingCreate"


class iot_ping_create:
    def __init__(self,temperature,humidity):
        self.temperature=temperature
        self.humidity=humidity
        
        self.public_ip = requests.get('https://api.ipify.org').text        
        self.date=str(datetime.datetime.now().isoformat())
        
    def iot_ping_create(self,temperature,humidity):
        global public_ip
        global iot_id
        global secretKey
        global local_ip
        global url
        
        try:
            
            payload = json.dumps({
            "iotUniqueId": iot_id,
            "clientPingTime": self.date,
            "serverPingTime": self.date,
            "humidity": self.humidity,
            "temperature": self.temperature,
            "localIP": local_ip,
            "publicIP": public_ip,
            "secretKey": secretKey
            })
            headers = {
            'Content-Type': 'application/json',
            }
            
            response = requests.request("POST", url, headers=headers, data=payload)
            
            res=response.json()
            print("ping result:", res["result"]["success"])
        
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
        