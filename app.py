import flask
from flask import Flask, render_template, redirect, url_for, request
from flask_table import Table, Col
from os import listdir
from os.path import isfile, join
import os, os.path
import numpy as np
import pandas as pd
import time, datetime
import subprocess
import pickle
import math
#from tkinter.filedialog import askopenfilename
from shutil import copyfile
from werkzeug import secure_filename
import glob, shutil
from sys import platform

app = Flask(__name__)

@app.route('/')
def index():
   return render_template("currencyapp.html")

   


if __name__ == '__main__':
	app.run(debug = True)
