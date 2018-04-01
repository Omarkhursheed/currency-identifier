from flask import Flask, render_template, redirect, url_for, request
from flaskext.mysql import MySQL
from os import listdir
from os.path import isfile, join

import os, os.path
import subprocess
import time, datetime
import glob, shutil

app = Flask(__name__)

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

dname = os.path.dirname(os.path.abspath(__file__))

def setup_database():
	global mysql
	mysql = MySQL()
	app.config['MYSQL_DATABASE_USER'] = 'omarkhursheed'
	app.config['MYSQL_DATABASE_PASSWORD'] = 'balloon16'
	app.config['MYSQL_DATABASE_DB'] = 'currency'
	app.config['MYSQL_DATABASE_HOST'] = 'localhost'
	mysql.init_app(app)


def query_db(query):
	query_string = """\
SELECT NAME, INFO, EXCHANGE_RATE from currency
WHERE NAME="{0}";""".format(query)
	conn = mysql.connect().cursor()
	conn.execute(query_string)
	out =  conn.fetchall()
	result = [(name, info, exchange_rate) for (name, info, exchange_rate) in out]
	x = result[0][0]
	y = result[0][1]
	z = result[0][2]
	if(x == 'us dollar'):
		x = 'US Dollar'
	elif(x == "indian rupee"):
		x = "Indian Rupee"
	elif(x == "saudi riyal"):
		x = "Saudi Riyal"
	return x, y, z



@app.route('/identify-currency', methods=['POST','GET'])
def teeth():

	for f in glob.glob("/Users/omarkhursheed/Downloads/img*.png"):
		os.remove(f)
	for f in glob.glob("/Users/omarkhursheed/Hack36/tf_files/img*.png") :
		os.remove(f)
	return render_template("teeth.html")


@app.route('/teethuploadcam',methods=['POST','GET'])
def teethuploadcam():
	if request.method == 'POST':
		temp=None
		
		for f in glob.glob("/Users/omarkhursheed/Downloads/img*.png"):
			temp = f

		print(temp)
		f = os.path.join(app.config['UPLOAD_FOLDER']+'/tf_files/', 'img.png')
		shutil.move(temp, os.path.join(app.config['UPLOAD_FOLDER']+'/tf_files/')+'img.png')

		subprocess.call("bash predict.sh png > result.txt", shell=True)
		filename = "result.txt"

		with open(filename, "r") as file:
			x = file.readlines()
		query = x[3].split(' ')[0]+' '+x[3].split(' ')[1]
		print(query)
		x, y, z = query_db(query)
		return render_template("result.html", x=x, y=y, z=z)

@app.route('/teethupload',methods=['POST','GET'])
def teethupload():
	if request.method == 'POST':
		myfile = request.files['image']

		z = myfile.filename
		ext = z.split('.')[-1]
		f = os.path.join(app.config['UPLOAD_FOLDER']+'/tf_files/', 'img.' + ext)
		myfile.save(f)
		ext=str(ext)
		subprocess.call("bash predict.sh "+ext+" > result.txt", shell=True)
		filename = "result.txt"

		file = open(filename, "r")

		x = file.readlines()
		query = x[3].split(' ')[0]+' '+x[3].split(' ')[1]
		x, y, z = query_db(query)
		return render_template("result.html", x=x, y=y, z=z)
		#return render_template("result.html", result=y)

@app.route('/')
def home():
	return render_template('hackapp.html')

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == '__main__':
	setup_database()
	app.run(debug = True)
