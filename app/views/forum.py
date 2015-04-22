from app import app
from flask import g, request, jsonify
import MySQLdb
import json
from utils import *
from user import getUserDict

@app.route('/db/api/forum/create/', methods=['POST'])
def forumCreate():	

	dataJSON = request.get_json(force = True)	
	try:		
		name = dataJSON['name']
		short_name = dataJSON['short_name']
		user = dataJSON['user']				
	except KeyError:
		return	jsonify(code = 3,	response = 'Missing parameters')

	try:
		query = "INSERT INTO forum (name, short_name, user) \
				 VALUES ('%s', '%s', '%s')" \
				 % (name, short_name, user) 
		cur = executeQuery(query)
		id = cur.lastrowid
	except MySQLdb.IntegrityError: 
		query = "SELECT id FROM forum \
				WHERE name='%s' OR short_name='%s'" \
				 % (name, short_name) 
		row = executeQuery(query).fetchone()
		id = row[0]
	
	return	jsonify(code = 0,	response = dict(
									id = id,	
									name = name, 
									short_name = short_name, 
									user = user
								))


@app.route('/db/api/forum/details/', methods=['GET'])
def forumDetails():
	forum = request.args.get('forum')	
	if not forum:
		return jsonify(code=3, response='Forum not specified')
	related = request.args.getlist('related')
	query = "SELECT id,name,short_name,user \
			 FROM forum \
			 WHERE short_name = '%s'" \
			 % (forum)
	row = executeQuery(query).fetchone()
	if not row:
		return	jsonify(code = 1, response = 'Not found')
	response = 	dict(
					id = row[0],	
					name = row[1], 
					short_name = row[2], 
					user = row[3]
				)	
	if 'user' in related:
		userDict = getUserDict(row[3])
		response['user'] = userDict

	return	jsonify(code = 0,	response = response)

@app.route('/db/api/forum/listThreads/')
def forumListThreads():
	return 'ok'

@app.route('/db/api/forum/listPosts/')
def forumListPosts():
	return 'ok'

@app.route('/db/api/forum/listUsers/')
def forumListUsers():
	return 'ok'
