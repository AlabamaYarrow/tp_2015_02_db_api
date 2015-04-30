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
		return	jsonify(code = 3,	response = 'Missing parameters')

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
		query = "SELECT id FROM post \
				WHERE ... " 
		#???



	return	jsonify(code = 0,	response = dict(
									date = date,
									forum = forum,
									id = id,	
									isApproved = isApproved,
									isDeleted = isDeleted,
									isEdited = isEdited,
									isHighlighted = isHighlighted,
									isSpam = isSpam,
									message = message,
									parent = parent,
									thread = thread,
									user = user
								))


@app.route('/db/api/post/details/', methods=['GET'])
def postDetails():	
	post = request.args.get('post')	
	if not post:
		return jsonify(code=3, response='Post not specified')	
	related = request.args.getlist('related')

	query = "SELECT date, isApproved, isDeleted, \
					isEdited, isHighlighted, \
			 		isSpam, message, parent,\
			 		thread, forum, user \
			 FROM post \
			 WHERE id = %s" 
	data = (post,)
	row = executeQueryData(query, data).fetchone()
	if not row:
		return	jsonify(code = 1, response = 'Not found')

	response = 	dict(					
					date = row[0].strftime("%Y-%m-%d %H:%M:%S"),
					isApproved = bool(row[1]),
					isDeleted = bool(row[2]),
					isEdited = bool(row[3]),
					isHighlighted = bool(row[4]),
					isSpam = bool(row[5]),
					message = row[6],
					parent = row[7],
					id = int(post),
					likes = 0,
					dislikes = 0,
					points = 0
				)	
	response['thread'] = row[8]
	response['forum'] = row[9]
	response['user'] = row[10]
	'''
	if 'thread' in related:
		response['thread'] = row[8]
	if 'forum' in related:
		response['forum'] = row[9]
	if 'user' in related:
		response['user'] = row[10]
	'''
	return	jsonify(code = 0,	response = response)


@app.route('/db/api/post/list/', methods=['GET'])
def listPosts():
	forum = request.args.get('forum')
	thread = request.args.get('thread')
	if not forum and not thread:
		return jsonify(code = 3, response = 'Incorrect response')

	since = request.args.get('since', '')
	limit = request.args.get('limit', -1)
	order = request.args.get('order', '')

	if forum:
		posts = getPostList(forum=forum, since=since, limit=limit, order=order)
	else:
		posts = getPostList(thread=thread, since=since, limit=limit, order=order)

	response = posts
	if response == None:
		response = []
	return jsonify(code = 0, response = response)


@app.route('/db/api/post/remove/', methods=['POST'])
def removePost():
	dataJSON = request.get_json(force = True)	
	try:
		postId = dataJSON['post']		
	except KeyError:
		return	jsonify(code = 3,	response = 'Missing parameters')
	post = getPostList(postId = postId)[0]
	threadId = post['thread']


	query = """UPDATE post SET isDeleted = 1 WHERE id = %s;"""
	data = (postId,)
	executeQueryData(query, data)

	postsInThreadDecrement(threadId)

	return jsonify(code = 0, response = {"post": postId})























