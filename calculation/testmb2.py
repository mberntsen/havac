#!/usr/bin/env python
#-*- coding: utf-8 -*-

import _mysql
import sys
import urllib2
import json
import math
import time

con = None
serverip = 'http://192.168.1.177'

timestamp = math.floor(time.time() / 60)
print "timestamp %d" % (timestamp)

#retrieve data: lichtsensor
try:
	req = urllib2.urlopen(serverip + '/lightsens/', timeout=4)
	data = json.loads(req.read())
	light = float(data['lightsens']) / 2.4
except urllib2.URLError as e:
	print e.reason  
	sys.exit(1)

#retrieve data: temperatures
try:
	req = urllib2.urlopen(serverip + '/tempsens/', timeout=4)
	data = json.loads(req.read())
	temp_indoor_ds  = float(data['indoor_ds'])
	temp_outdoor    = float(data['outdoor'])
	temp_metering   = float(data['metering'])
except urllib2.URLError as e:
	print e.reason  
	sys.exit(1)

#retrieve data: pressures
try:
	req = urllib2.urlopen(serverip + '/presssens/', timeout=4)
	data = json.loads(req.read())
	press_indoor = float(data['indoor']) / 100
except urllib2.URLError as e:
	print e.reason  
	sys.exit(1)

#retrieve data: cv data
try:
	req = urllib2.urlopen(serverip + '/cv/', timeout=4)
	data = json.loads(req.read())
	cv_state = float(data['state'])
	warmte = float(data['warmte'])
	T1 = float(data['T1'])
	T2 = float(data['T2'])
except urllib2.URLError as e:
	print e.reason  
	sys.exit(1)

#retrieve data: humidity
try:
	req = urllib2.urlopen(serverip + '/rhsens/', timeout=4)
	data = json.loads(req.read())
	rh_indoor = float(data['indoor'])
except urllib2.URLError as e:
	print e.reason  
	sys.exit(1)

#save all to database
try:
	con = _mysql.connect('localhost', 'python', 'python', 'test')
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 100, %.2f, 'mb light')" % (timestamp, light))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 102, %.2f, 'mb outdoor')" % (timestamp, temp_outdoor))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 103, %.2f, 'mb metering')" % (timestamp, temp_metering))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 104, %.2f, 'mb indoor_ds')" % (timestamp, temp_indoor_ds))
#	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 105, %.2f, 'mb indoor_bmp')" % (timestamp, temp_indoor_bmp))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 120, %.2f, 'mb pressure')" % (timestamp, press_indoor))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 130, %.2f, 'mb cv state')" % (timestamp, cv_state))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 131, %.2f, 'mb cv Warmte')" % (timestamp, warmte))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 132, %.2f, 'mb cv T1')" % (timestamp, T1))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 133, %.2f, 'mb cv T2')" % (timestamp, T2))
	con.query("INSERT INTO metingen (tijd3, sensorid, waarde, comment) VALUES (%d, 140, %.2f, 'mb relative humidity')" % (timestamp, rh_indoor))
except _mysql.Error as e:
	print e.reason
	sys.exit(1)
finally:
	if con:
		con.close()

