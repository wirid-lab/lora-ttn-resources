#!/usr/bin/python
# -*- coding: utf-8 -*-
import serial
import os
import time
ser=serial.Serial("/dev/ttyUSB0",115200)
time.sleep(0.5)
ser.write(b'at+help\r\n')
time.sleep(0.5)
ser.write(b'at+version\r\n')
time.sleep(0.5)
ser.write(b'at+get_config=device:status\r\n')
time.sleep(0.5)
ser.write(b'at+get_config=lora:work_mode:0\r\n') ##0 LoRaWAN ; 1 LoRaP2P ; 2 Test M$
time.sleep(0.5)
ser.write(b'at+set_config=lora:region:US915\r\n') ##
time.sleep(0.5)
ser.write(b'at+set_config=lora:join_mode:1\r\n') ## 0: OTAA, 1: ABP
time.sleep(0.5)
ser.write(b'at+set_config=lora:class:0\r\n') ## class 0 class A; 1 class B; 2 class$
time.sleep(0.5)
#ser.write(b'at+set_config=lora:confirm:1\r\n') ## 0: unconfirm, 1: confirm
#time.sleep(0.5)
ser.write(b'at+set_config=lora:dev_addr:01586114\r\n') ##
time.sleep(0.5)
ser.write(b'at+set_config=lora:nwks_key:ce0376e3796578d57e328a05cf41977c\r\n')
time.sleep(0.5)
ser.write(b'at+set_config=lora:apps_key:520c6561b1a1dc1707f92b23fd2abff4\r\n')
time.sleep(0.5)
#ser.write(b'at+set_config=lora:adr:0\r\n') ## 0: Close ADR, 1: Open ADR.
#time.sleep(0.5)
ser.write(b'at+set_config=lora:dr:3\r\n') ##  the number of DR. Generally, the valu$
time.sleep(0.5)
ser.write(b'at+set_config=lora:send_interval:1:30\r\n')
time.sleep(0.5)
ser.write(b'at+join\r\n')
time.sleep(0.5)
readedText = ser.readline()
print(readedText)
ser.close()


