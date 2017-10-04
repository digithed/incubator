from flask import Flask, render_template, json, request, url_for, session, redirect
from flask_pymongo import PyMongo
import bcrypt
import time
from datetime import datetime
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

app = Flask(__name__)

app.config['MONGO_DBNAME'] = #removed for confidentiality purposes
app.config['MONGO_URI'] = #removed for confidentiality purposes
mongo = PyMongo(app)

hey = datetime.now()
posttime = datetime.now()
numofposts = [0]


@app.route("/")
def index():
	return render_template('index.html')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
	if request.method == 'POST':
		users = mongo.db.users
		existing_user = users.find_one({'name' : request.form['inputName']})

		if existing_user is None:
			hashpass = bcrypt.hashpw(request.form['inputPassword'].encode('utf-8'), bcrypt.gensalt())
			users.insert({'name': request.form['inputName'], 'password': hashpass, 'email': request.form['inputEmail']})
			session['inputName']= request.form['inputName']
			hey = datetime.now()
			return redirect(url_for('home'))
			
		return render_template('error.html')
	return render_template('signup.html')

@app.route("/signin", methods=['POST', 'GET'])
def signin():
	if request.method == 'POST':
		users = mongo.db.users
		login_user = users.find_one({'name' : request.form['inputName']})

		if login_user:
			if bcrypt.hashpw(request.form['inputPassword'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
				session['inputName']= request.form['inputName']
				return redirect(url_for('home'))

		return render_template('error2.html')
	return render_template('signin.html')

#@app.route("/success")
#def success():
	#if 'inputName' in session:
		#return redirect(url_for('home'))
		#print ('You are logged in as ' + session['inputName'])
		

@app.route("/home")
def home():
	username = session['inputName']
	return render_template('home.html', home=username)

@app.route("/profile")
def profile():
	username = session['inputName']
	return render_template('profile.html', numofposts=numofposts[0], now=hey, home=username)

#Currently using the 'Writing' page to test post-matching based on similarity of strings
@app.route("/writing", methods=['POST', 'GET'])
def writing():
	data = mongo.db.posts
	if request.method == 'POST' and data.find_one({'post': request.form['say']}):
		alert = 'Another user has said something similar to you: '
		#ratio = fuzz.partial_ratio(data.collection.find(), request.form['say'])
		simsg = data.find_one({'post': request.form['say']})
		return render_template('writing.html', alert=alert, simsg=simsg) #ratio=ratio)

	if request.method == 'POST':
		data = mongo.db.posts
		data.insert({'user': session['inputName'], 'post': request.form['say']})
		at = 'At'
		text = 'posted: '
		posttime = datetime.now()
		post = request.form['say']
		username = session['inputName']
		numofposts[0] += 1
		return render_template('writing.html', at=at, text=text, posted=post, time=posttime, home=username)
	
	return render_template('writing.html')


@app.route("/philosophy", methods=['POST', 'GET'])
def philosophy():
	if request.method == 'POST':
		at = 'At'
		text = 'posted: '
		posttime = datetime.now()
		post = request.form['say']
		username = session['inputName']
		numofposts[0] += 1
		return render_template('philosophy.html', at=at, text=text, posted=post, time=posttime, home=username)
	return render_template('philosophy.html')

@app.route("/computers", methods=['POST', 'GET'])
def computers():
	if request.method == 'POST':
		at = 'At'
		text = 'posted: '
		posttime = datetime.now()
		post = request.form['say']
		username = session['inputName']
		numofposts[0] += 1
		return render_template('computers.html', at=at, text=text, posted=post, time=posttime, home=username)
	return render_template('computers.html')

if __name__ == "__main__":
	app.secret_key = #removed for confidentiality purposes
	app.run()
