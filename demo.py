
# -*- coding: utf-8 -*-
#!/usr/bin/env python
import time
import serial
import re
import os
import string
import commands
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)


enable_pin = 2
coil_A_1_pin = 5
coil_A_2_pin = 6
coil_B_1_pin = 12
coil_B_2_pin = 13

#
coil_C_1_pin = 17
coil_C_2_pin = 18
coil_D_1_pin = 22
coil_D_2_pin = 23




GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)

#
GPIO.setup(coil_C_1_pin, GPIO.OUT)
GPIO.setup(coil_C_2_pin, GPIO.OUT)
GPIO.setup(coil_D_1_pin, GPIO.OUT)
GPIO.setup(coil_D_2_pin, GPIO.OUT)


GPIO.output(enable_pin, 1)

def plane_forward(delay, steps):
  for i in range(0, steps):
    plane_setStep(1, 0, 0, 0)
    time.sleep(delay)
    plane_setStep(0, 1, 0, 0)
    time.sleep(delay)
    plane_setStep(0, 0, 1, 0)
    time.sleep(delay)
    plane_setStep(0, 0, 0, 1)
    time.sleep(delay)

def vertical_forward(delay, steps):
  for i in range(0, steps):
    vertical_setStep(1, 0, 0, 0)
    time.sleep(delay)
    vertical_setStep(0, 1, 0, 0)
    time.sleep(delay)
    vertical_setStep(0, 0, 1, 0)
    time.sleep(delay)
    vertical_setStep(0, 0, 0, 1)
    time.sleep(delay)

def plane_backwards(delay, steps):
  for i in range(0, steps):
    plane_setStep(0, 0, 0, 1)
    time.sleep(delay)
    plane_setStep(0, 0, 1, 0)
    time.sleep(delay)
    plane_setStep(0, 1, 0, 0)
    time.sleep(delay)
    plane_setStep(1, 0, 0, 0)
    time.sleep(delay)

def vertical_backwards(delay, steps):
  for i in range(0, steps):
    vertical_setStep(0, 0, 0, 1)
    time.sleep(delay)
    vertical_setStep(0, 0, 1, 0)
    time.sleep(delay)
    vertical_setStep(0, 1, 0, 0)
    time.sleep(delay)
    vertical_setStep(1, 0, 0, 0)
    time.sleep(delay)

def vertical_setStep(w5, w6, w7, w8):
  GPIO.output(coil_C_1_pin, w5)
  GPIO.output(coil_C_2_pin, w6)
  GPIO.output(coil_D_1_pin, w7)
  GPIO.output(coil_D_2_pin, w8)

def plane_setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

delay = 5
mediu = 512/360 

ser = serial.Serial("/dev/ttyUSB0", 38400, timeout=1)
str = ser.read(88)
#匹配
juj = '^-y.*?500$'

n = 10
plane_steps = 0
vertical_steps = 0
while n :
	time.sleep(1)
	if(n):
		print "从服务器收到的数据:",str
		justr = re.match('^-y.*?',str)
		if justr:
			var =  os.popen('sudo python test2hmc.py').read()
			
			print "数据接受正确"
			
			print "正在计算此时的三维信息:",var
			print "数据处理阶段："
			mh1 = re.search('(\(.*\,).*',var)
			mh2 = re.search('.*(\,.*\))',var)
			pattern = re.compile(r'\d+.\d+')
			for m in re.finditer(pattern,mh1.group(1)):
				temp1 = m.group()
        		for m in re.finditer(pattern,mh2.group(1)):
				temp2 = m.group()
			print "现在的板子方位角为：",temp1
			print "现在的板子高度角为：",temp2
			vs = os.popen('./sopo-master/sopo %s'%(str)).read()
			print "现在计算太阳天文信息",vs
			print "正在解析数据。。。"
			reazi1 = re.search('(azi\"\:.*\,\"zen)',vs)
			zenit1 = re.search('(zen\"\:.*\,\"inc)',vs)

			for m in re.finditer(pattern,reazi1.group(1)):
        			temp3 = m.group()
			for m in re.finditer(pattern,zenit1.group(1)):
        			temp4 = m.group()
			print "获得此刻的太阳方位角为：",temp3
			print "获得此刻的太阳高度角为：",temp4
			planetemp = float(temp3)-float(temp1)
			verticaltemp = float(temp4)-float(temp2)
			print "此时水平方向需要矫正度数：",planetemp
			print "此时竖直方向需要矫正度数：",verticaltemp
		
			plane_steps = mediu * planetemp
			vertical_steps = mediu * verticaltemp
			if temp3>0:
				print "水平方向旋转%d"%plane_steps
				plane_forward(int(delay)/1000.0,int(plane_steps))
			else:
				print "水平方向旋转%d"%plane_steps
				plane_backwards(int(delay)/1000.0,int(plane_steps))
			if temp4>0:
				print "竖直方向旋转%d"%vertical_steps
				vertical_forward(int(delay)/1000.0,int(vertical_steps))
			else:
				print "数值方向旋转%d"%vertical_steps
				vertical_backwards(int(delay)/1000.0,int(vertical_steps))			
											
			
			
			break
			
		else:
			print "数据有误，请重新从服务器发送数据"
			break
		n = n - 1
	
print "流程完成！"
