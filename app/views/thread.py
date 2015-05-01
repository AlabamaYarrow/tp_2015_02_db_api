from app import app
from flask import g, request, jsonify
import MySQLdb
from utils import *

from post import postRemove, postRestore


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
		return	jsonify(code = 3, response = 'Missing parameters')
	
	isDeleted = dataJSON.get('isDeleted', False)

	try:		
		query = "INSERT INTO thread (forum, title, \
				isClosed, user, date, message, \
				slug, isDeleted) \
				VALUES (%s, %s, %s, %s, %s, %s, %s, %s)" 
		data = (forum, title, int(isClosed), user, date, \
				message, slug, int(isDeleted) )
		cur = executeQueryData(query, data)
		id = cur.lastrowid
	except MySQLdb.IntegrityError: 
		return	jsonify(code = 5, response = 'Already exists')

	response = {
		'forum' : forum,
		'title' : title,
		'isClosed' : isClosed,
		'user' : user,
		'date' : date,
		'message' : message,
		'slug' : slug,
		'isDeleted' : isDeleted,																		
		'id' : id
	}

	return	jsonify(code = 0, response = response)


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

	response = {					
		'date' : row[0].strftime("%Y-%m-%d %H:%M:%S"), 
		'dislikes' : int(row[1]),
		'id' : int(thread),
		'isClosed' : bool(row[2]),
		'isDeleted' : bool(row[3]),
		'likes' : int(row[4]),
		'message' : row[5],
		'points' : int(row[6]),										
		'posts' : int(row[7]),
		'slug' : row[8],
		'title' : row[9]				
	}
	response['forum'] = row[10]
	response['user'] = row[11]	

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
		threads = getThreadList(forum=forum, since=since, order=order, limit=limit)
	else:
		threads = getThreadList(user=user, since=since, order=order, limit=limit)

	response = threads
	if response == None:
		response = []

	return jsonify(code = 0, response = response)


@app.route('/db/api/thread/listPosts/', methods=['GET'])
def threadListPosts():
	thread = request.args.get('thread')
	since = request.args.get('since', '')
	limit = request.args.get('limit', -1)
	order = request.args.get('order', 'desc')
	sort = request.args.get('sort', 'flat')

	posts = getPostList(thread = thread, since = since, limit = limit, \
						sort = sort, order = order)
	response = posts
	if response == None:
		response = []	

	return jsonify(code = 0, response = response)	


@app.route('/db/api/thread/remove/', methods=['POST'])
def threadRemove():
	dataJSON = request.get_json()	
	try:
		threadId = dataJSON['thread']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')

	query = "UPDATE thread SET isDeleted = 1 WHERE id = %s;" 
	data = (threadId,)
	executeQueryData(query, data)

	posts = getPostList(thread = threadId)
	for post in posts:
		postRemove(post['id'])

	return jsonify(code = 0, response = threadId)


@app.route('/db/api/thread/restore/', methods=['POST'])
def threadRestore():
	dataJSON = request.get_json()	
	try:
		threadId = dataJSON['thread']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')

	query = "UPDATE thread SET isDeleted = 0 WHERE id = %s;" 
	data = (threadId,)
	executeQueryData(query, data)

	posts = getPostList(thread = threadId)
	for post in posts:
		postRestore(post['id'])

	return jsonify(code = 0, response = threadId)


@app.route('/db/api/thread/close/', methods=['POST'])
def threadClose():
	dataJSON = request.get_json()	
	try:
		threadId = dataJSON['thread']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')	

	query = "UPDATE thread SET isClosed = 1 WHERE id = %s;"
	data = (threadId,)
	executeQueryData(query, data)

	return jsonify(code = 0, response = threadId)


@app.route('/db/api/thread/open/', methods=['POST'])
def threadOpen():
	dataJSON = request.get_json()	
	try:
		threadId = dataJSON['thread']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')	

	query = "UPDATE thread SET isClosed = 0 WHERE id = %s;"
	data = (threadId,)
	executeQueryData(query, data)

	return jsonify(code = 0, response = threadId)


@app.route('/db/api/thread/update/', methods=['POST'])
def threadUpdate():
	dataJSON = request.get_json()	
	try:
		threadId = dataJSON['thread']
		message = dataJSON['message']
		slug = dataJSON['slug']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')	

	query = "UPDATE thread SET message = %s, slug = %s WHERE id = %s;"
	data = (message, slug, threadId)
	executeQueryData(query,data)

	threads = getThreadList(threadId = threadId)
	if threads != list():
		thread = threads[0]
	else:
		thread = dict()

	return jsonify(code = 0, response = thread)


@app.route('/db/api/thread/vote/', methods=['POST'])
def threadVote():
	dataJSON = request.get_json()	
	try:
		threadId = dataJSON['thread']
		vote = dataJSON['vote']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')	

	if vote == 1:
		query = "UPDATE thread SET likes = likes + 1, points = points + 1 WHERE id = %s;"
	else:
		query = "UPDATE thread SET dislikes = dislikes + 1, points = points - 1 WHERE id = %s;"
	data = (threadId,)
	executeQueryData(query,data)

	threads = getThreadList(threadId = threadId)
	if threads != list():
		thread = threads[0]
	else:
		thread = dict()

	return jsonify(code = 0, response = thread)


@app.route('/db/api/thread/subscribe/', methods=['POST'])
def threadSubscribe():
	dataJSON = request.get_json()
	try:
		user = dataJSON['user']
		thread = dataJSON['thread']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')

	query = "INSERT INTO subscription (subscriber, thread) VALUES (%s, %s);"
	data = (user,thread)
	executeQueryData(query,data)

	response = {'thread' : thread, 'user' : user}

	return jsonify(code = 0, response = response)


@app.route('/db/api/thread/unsubscribe/', methods=['POST'])
def threadUnsubscribe():
	dataJSON = request.get_json()
	try:
		user = dataJSON['user']
		thread = dataJSON['thread']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')

	query = "DELETE FROM subscription \
				WHERE subscriber = %s AND thread = %s;"
	data = (user,thread)
	executeQueryData(query,data)

	response = {'thread' : thread, 'user' : user}

	return jsonify(code = 0, response = response)	


