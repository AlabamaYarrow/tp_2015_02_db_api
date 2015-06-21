from app import app
from flask import g, request, jsonify
import MySQLdb
from utils import *


@app.route('/db/api/post/create/', methods=['POST'])
def postCreate():	
	dataJSON = request.get_json(force = True)	
	try:
		date = dataJSON['date']
		thread = dataJSON['thread']
		message = dataJSON['message']
		user = dataJSON['user']
		forum = dataJSON['forum']
	except KeyError:
		return	jsonify(code = 3, response = 'Missing parameters')

	parent = dataJSON.get('parent', None)
	isApproved = dataJSON.get('isApproved', False)
	isHighlighted = dataJSON.get('isHighlighted', False)
	isEdited = dataJSON.get('isEdited', False)
	isSpam = dataJSON.get('isSpam', False)
	isDeleted = dataJSON.get('isDeleted', False)

	try:		
		query = "INSERT INTO post (date, thread, message, user, forum, parent, \
									isApproved, isHighlighted, isEdited, isSpam, isDeleted) \
				 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" 
		data = (date, thread, message, user, forum, parent, \
				int(isApproved), int(isHighlighted), int(isEdited), int(isSpam), int(isDeleted))
		cur = executeQueryData(query, data)
		id = cur.lastrowid
		postsInThreadIncrement(thread)
	except MySQLdb.IntegrityError: 
		return	jsonify(code = 5, response = 'Already exists')

	response = {
		'date' : date,
		'forum' : forum,
		'id' : id,	
		'isApproved' : isApproved,
		'isDeleted' : isDeleted,
		'isEdited' : isEdited,
		'isHighlighted' : isHighlighted,
		'isSpam' : isSpam,
		'message' : message,
		'parent' : parent,
		'thread' : thread,
		'user' : user
	}

	return	jsonify(code = 0, response = response)


@app.route('/db/api/post/details/', methods=['GET'])
def postDetails():	
	post = request.args.get('post')	
	if not post:
		return jsonify(code = 3, response = 'Post not specified')	
	related = request.args.getlist('related')

	query = "SELECT date, isApproved, isDeleted, \
					isEdited, isHighlighted, \
			 		isSpam, message, parent,\
			 		likes, dislikes, points,\
			 		thread, forum, user \
			 FROM post \
			 WHERE id = %s" 
	data = (post,)
	row = executeQueryData(query, data).fetchone()
	if not row:
		return	jsonify(code = 1, response = 'Not found')

	response = {					
		'date' : row[0].strftime("%Y-%m-%d %H:%M:%S"),
		'isApproved' : bool(row[1]),
		'isDeleted' : bool(row[2]),
		'isEdited' : bool(row[3]),
		'isHighlighted' : bool(row[4]),
		'isSpam' : bool(row[5]),
		'message' : row[6],
		'parent' : row[7],
		'id' : int(post),
		'likes' : int(row[8]),
		'dislikes' : int(row[9]),
		'points' : int(row[10])
	}	
	response['thread'] = row[11]
	response['forum'] = row[12]
	response['user'] = row[13]

	return	jsonify(code = 0, response = response)


@app.route('/db/api/post/list/', methods=['GET'])
def listPosts():
	forum = request.args.get('forum')
	thread = request.args.get('thread')
	if not forum and not thread:
		return jsonify(code = 3, response = 'Missing parameters')

	since = request.args.get('since', '')
	limit = request.args.get('limit', -1)
	order = request.args.get('order', '')

	if forum:
		posts = getPostList(forum = forum, since = since, limit = limit, order = order)
	else:
		posts = getPostList(thread = thread, since = since, limit = limit, order = order)

	response = posts
	if response == None:
		response = []
	return jsonify(code = 0, response = response)


@app.route('/db/api/post/remove/', methods=['POST'])
def postRemove(postId = 0):
	if not postId:
		dataJSON = request.get_json(force = True)	
		try:
			postId = dataJSON['post']		
		except KeyError:
			return	jsonify(code = 3,	response = 'Missing parameters')
	post = getPostList(postId = postId)[0]
	threadId = post['thread']

	query = "UPDATE post SET isDeleted = 1 WHERE id = %s;"
	data = (postId,)
	executeQueryData(query, data)

	postsInThreadDecrement(threadId)

	return jsonify(code = 0, response = {"post": postId})


@app.route('/db/api/post/restore/', methods=['POST'])
def postRestore(postId = 0):
	if not postId:
		dataJSON = request.get_json(force = True)	
		try:
			postId = dataJSON['post']		
		except KeyError:
			return	jsonify(code = 3,	response = 'Missing parameters')
	post = getPostList(postId = postId)[0]
	threadId = post['thread']

	query = "UPDATE post SET isDeleted = 0 WHERE id = %s;"
	data = (postId,)
	executeQueryData(query, data)

	postsInThreadIncrement(threadId)

	return jsonify(code = 0, response = {"post": postId})



@app.route('/db/api/post/update/', methods=['POST'])
def postUpdate():
	dataJSON = request.get_json(force = True)	
	try:
		postId = dataJSON['post']
		message = dataJSON['message']
	except KeyError:
		return	jsonify(code = 3,	response = 'Missing parameters')

	query = "UPDATE post SET message = %s WHERE id = %s;"
	data = (message, postId)

	executeQueryData(query,data)

	posts = getPostList(postId = postId)
	if not posts:
		return jsonify(code = 1, response = [])
	elif not posts[0]:
		return jsonify(code = 1, response = [])

	return jsonify(code = 0, response = posts[0])


@app.route('/db/api/post/vote/', methods=['POST'])
def postVote():
	dataJSON = request.get_json()
	try:
		postId = dataJSON['post']
		vote = dataJSON['vote']
	except KeyError:
		return jsonify(code = 3, response = 'Missing parameters')

	if vote == 1:
		query = "UPDATE post SET likes = likes + 1, points = points + 1 WHERE id = %s;"
	elif vote == -1:
		query = "UPDATE post SET dislikes = dislikes + 1, points = points - 1 WHERE id = %s;"
	else:
		return jsonify(code =  3, response = 'Incorrect vote')

	data = (postId,)
	executeQueryData(query, data)

	posts = getPostList(postId = postId)
	if not posts:
		return jsonify(code = 1, response = [])
	elif not posts[0]:
		return jsonify(code = 1, response = [])

	return jsonify(code = 0, response = posts[0])














