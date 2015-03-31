from app import app
from flask import g, request, jsonify
import MySQLdb
from utils import *


@app.route('/db/api/user/create', methods=['POST'])
def userCreate():	
	
	dataJSON = request.get_json(force = True)	
	try:		
		name = dataJSON['name']
		about = dataJSON['about']
		username = dataJSON['username']
		email = dataJSON['email']
		isAnonymousString = dataJSON.get('isAnonymous') 
		isAnonymous = None 
		if isAnonymousString == 'true':
			isAnonymous = 1
		elif isAnonymousString == 'false':
			isAnonymous = 0		
	except KeyError:
		return	jsonify(code = 3,	response = 'Missing parameters')
	
	try:
		query = "INSERT INTO user (name, about, username, email, isAnonymous) \
				 VALUES ('%s', '%s', '%s', '%s', '%s')" \
				 % (name, about, username, email, isAnonymous) 
		cur = executeQuery(query)
	except MySQLdb.IntegrityError: 
		return jsonify(code = 5,	response = 'User exists')
	
	return	jsonify(code = 0,	response = dict(
									id = cur.lastrowid,	
									name = name, 
									about = about, 
									username = username,
									email = email,
									isAnonymous = isAnonymous
								))
	