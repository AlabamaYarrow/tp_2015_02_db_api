from app import app
from flask import g, request, jsonify
from utils import *

@app.route('/', methods=['GET'])
@app.route('/db/api/', methods=['GET'])
def index():
	return 'Hello world!'


@app.route('/db/api/status/', methods=['GET'])
def status():	
	query = 'SELECT \
			(SELECT COUNT(id) \
			FROM user),\
			(SELECT COUNT(id) \
			FROM thread),\
			(SELECT COUNT(id) \
			FROM forum),\
			(SELECT COUNT(id) \
			FROM post)'
						
	cur = executeQuery(query)	
	r = cur.fetchone()
	response = {
		'user' : r[0],
		'thread' : r[1],
		'forum' : r[2],
		'post' : r[3] 
	}

	return jsonify (code = 0, response = response)


@app.route('/db/api/clear/', methods=['POST'])
def clear():	
	query = 'TRUNCATE TABLE user'
	executeQuery(query)	
	query = 'TRUNCATE TABLE thread'
	executeQuery(query)	
	query = 'TRUNCATE TABLE forum'
	executeQuery(query)	
	query = 'TRUNCATE TABLE post'
	executeQuery(query)	
	query = 'TRUNCATE TABLE follower'
	executeQuery(query)	
	query = 'TRUNCATE TABLE subscription'
	executeQuery(query)	
	
	return jsonify (code = 0, response = 'OK')

