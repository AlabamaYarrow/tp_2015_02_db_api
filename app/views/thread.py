from app import app
from flask import g, request, jsonify
import MySQLdb
from utils import *


@app.route('/db/api/thread/create/', methods=['POST'])
def threadCreate():	
	dataJSON = request.get_json(force = True)	
	try:
		forum = dataJSON['forum']
		title = dataJSON['title']
		isClosed = dataJSON['isClosed']
		user = dataJSON['user']
		date = dataJSON['date']
		message = dataJSON['message']
		slug = dataJSON['slug']
	except KeyError:
		return	jsonify(code = 3,	response = 'Missing parameters')

	isDeleted = dataJSON.get('isDeleted', False)
	
	try:		
		query = "INSERT INTO thread (forum, title, isClosed, user, date, message, \
									slug, isDeleted) \
				 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" 
		data = (forum, title, int(isClosed), user, date, message, \
				slug, int(isDeleted))
		cur = executeQueryData(query, data)
		id = cur.lastrowid
	except MySQLdb.IntegrityError: 
		query = "SELECT id FROM thread \
				WHERE ... "
		#???

	return	jsonify(code = 0,	response = dict(
									forum = forum,
									title = title,
									isClosed = isClosed,
									user = user,
									date = date,
									message = message,
									slug = slug,
									isDeleted = isDeleted,																		
									id = id
								))


@app.route('/db/api/thread/details/', methods=['GET'])
def threadDetails():	
	thread = request.args.get('thread')	
	if not thread:
		return jsonify(code=3, response='Thread not specified')	
	related = request.args.getlist('related')
	forumInRelated = False
	userInRelated = False
	for relatedValue in related:
		if relatedValue == 'forum':
			forumInRelated = True
		elif relatedValue == 'user':
			userInRelated = True
		else:
			return	jsonify(code = 3, response = 'Incorrect request')

	query = "SELECT date, dislikes, isClosed, isDeleted, likes, \
					message, points, posts, slug, title, forum, user \
			 FROM thread \
			 WHERE id = %s" 
	data = (thread,)
	row = executeQueryData(query, data).fetchone()
	if not row:
		return	jsonify(code = 1, response = 'Not found')

	response = 	dict(					
					date = row[0].strftime("%Y-%m-%d %H:%M:%S"), # slow?
					dislikes = int(row[1]),
					id = int(thread),
					isClosed = bool(row[2]),
					isDeleted = bool(row[3]),
					likes = int(row[4]),
					message = row[5],
					points = int(row[6]),										
					posts = int(row[7]),
					slug = row[8],
					title = row[9]
				)	
	print response
	
	response['forum'] = row[10]
	response['user'] = row[11]
	'''
	if forumInRelated:
		response['forum'] = row[6]
	if userInRelated:
		response['user'] = row[7]
	'''
	return	jsonify(code = 0,	response = response)


@app.route('/db/api/thread/list/', methods=['GET'])
def threadList():
	forum = request.args.get('forum') 
	user = request.args.get('user')
	if not forum and not user:
		return jsonify(code = 3, response = 'Missing parameters')

	since = request.args.get('since', '')
	order = request.args.get('order', '')
	limit = request.args.get('limit', -1)

	if request.args.get('forum'):
		threads = getThreads(forum=forum, since=since, order=order, limit=limit)
	else:
		threads = getThreads(user=user, since=since, order=order, limit=limit)

	response = threads
	if response == None:
		response = []
	return jsonify(code = 0, response = response)

@app.route('/db/api/thread/listPosts/', methods=['GET'])
def threadListPosts():
	
	response = []
	return jsonify(code = 0, response = response)	





