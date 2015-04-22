from app import app
from flask import g, request, jsonify
import MySQLdb
import json
from utils import *


@app.route('/db/api/user/create/', methods=['POST'])
def userCreate():	
	dataJSON = request.get_json(force = True)	
	try:		
		name = dataJSON['name']
		about = dataJSON['about']
		username = dataJSON['username']
		email = dataJSON['email']	
		isAnonymous = dataJSON.get('isAnonymous', False) 
	except KeyError:
		return	jsonify(code = 3,	response = 'Missing parameters')
	
	try:
		query = "INSERT INTO user (name, about, username, email, isAnonymous) \
				 VALUES (%s, %s, %s, %s, %s)" 
		data = (name, about, username, email, int(isAnonymous)) 
		cur = executeQueryData(query, data)
	except MySQLdb.IntegrityError: 
		return jsonify(code = 5, response = 'User exists')

	return	jsonify(code = 0,	response = dict(
									id = cur.lastrowid,	
									name = name, 
									about = about, 
									username = username,
									email = email,
									isAnonymous = isAnonymous
								))

@app.route('/db/api/user/details/', methods=['GET'])
def userDetails(): 	
	try:		
		user = request.args.get('user')
	except KeyError:
		return	jsonify(code = 3,	response = 'User not specified')

	response = getUserDict(user)
	if response == 'Not Found':
		return jsonify(code = 1, response = response)
		
	return	jsonify(code = 0, response = response)

def getUserDict(user):
	query = "SELECT id, email, username, name, isAnonymous, about \
			 FROM user \
			 WHERE email = %s" 
	data = (user,)
	cur = executeQueryData(query, data)
	row = cur.fetchone()
	if not row:
		return 'Not found'

	return {
				'id' : row[0],
				'email' : row[1],
				'username' : row[2],
				'name' : row[3],
				'isAnonymous' : bool(row[4]),
				'about' : row[5],				
				'followers' : [],
				'following' : [],
				'subscriptions' : []				
			}