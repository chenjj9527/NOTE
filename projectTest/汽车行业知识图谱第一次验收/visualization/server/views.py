# -*- coding: utf-8 -*-

import os
import time

from flask import request,render_template
from server.app import app
from server import models
from server import mysql

database=mysql.database()
mydata = ""

@app.route("/api/v1", methods=["GET"])
def parse():
	global mydata
	req = request.args
	# .args.get('username')
	if "car_name" in req:
		name = req["car_name"]
		mydata = models.execute(database,("car_name", name))
	'''
	elif "relation" in req:
		name = req["relation"]
		mydata = models.execute(database,("relation", name))	
	'''	
	# return {"resultmsg":"OK","resultno":ERROR_OK},200
	# 模板的位置放在templates文件夹下面
	return render_template('index.html')

@app.route("/api/data")
def data():
	return mydata

