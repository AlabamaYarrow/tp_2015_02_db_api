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
				 VALUES (%s, %s, %s)" 
		data = (name, short_name, user) 
		cur = executeQueryData(query, data)
		id = cur.lastrowid
	except MySQLdb.IntegrityError: 
		query = "SELECT id FROM forum \
				WHERE name=%s OR short_name=%s"
		data = (name, short_name) 
		row = executeQueryData(query, data).fetchone()
		id = row[0]
	
	return	jsonify(code = 0,	response = 	dict(
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
			 WHERE short_name = %s" 
	data = (forum,)
	row = executeQueryData(query,data).fetchone()
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


@app.route('/db/api/forum/listThreads/', methods=['GET'])
def forumListThreads():
	forum = request.args.get('forum')
	if not forum:
		return	jsonify(code = 3,	response = 'Missing parameters')		
	since = request.args.get('since', '')
	limit = request.args.get('limit', -1)
	order = request.args.get('order', 'desc')
	related = request.args.getlist('related')

	threads = getThreads(forum=forum, since=since, order=order, limit=limit)

	for thread in threads:
		if 'user' in related:
			thread['user'] = getUserDict(thread['user'])
			thread['user']['followers'] = getFollowersList(thread['user']['email'])
			thread['user']['following'] = getFollowingList(thread['user']['email'])
			thread['user']['subscriptions'] = getSubscribedThreadsList(thread['user']['email'])

		if 'forum' in related:
			thread['forum'] = getForumDict(short_name=thread['forum'])
	return	jsonify(code = 0,	response = threads)


@app.route('/db/api/forum/listPosts/')
def forumListPosts():

	return	jsonify(code = 0,	response = posts)


@app.route('/db/api/forum/listUsers/')
def forumListUsers():
	return 'ok'
