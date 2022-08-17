# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 13:29:15 2022

@author: myc
"""

import threading
import serial_data

def main():
    start=True
    serial_data_object=serial_data.serial_data(start)
    t1=threading.Thread(target=serial_data_object.serial_data, args=(start,))
    t1.start()
        
if __name__== '__main__':
    main()