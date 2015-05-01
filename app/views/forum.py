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
	forumDict = getForumDict(forum)

	if 'user' in related:
		userDict = getUserDict(forumDict['user'])
		forumDict['user'] = userDict

	response = forumDict

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
			thread['forum'] = getForumDict(thread['forum'])
	return	jsonify(code = 0,	response = threads)


@app.route('/db/api/forum/listUsers/', methods=['GET'])
def forumListUsers():
	forum = request.args.get('forum')
	if not forum:
		return jsonify(code = 3, response = 'Missing parameters')

	sinceId = request.args.get('since_id')
	if sinceId:
		try:
			sinceId = int(sinceId)
		except ValueError:
			return jsonify(code = 3, response = 'Incorrect request')
		sinceIdCond = """AND user.id >= {}""".format(sinceId)
	else:
		sinceIdCond = ''

	if request.args.get('limit'):
		limit = request.args.get('limit')
		try:
			limit = int(limit)
		except ValueError:
			return jsonify(code = 3, response = 'Incorrect request')
		if limit < 0:
			return jsonify(code = 3, response = 'Incorrect request')
		limitCond = """LIMIT {}""".format(limit)
	else:
		limitCond = ''

	order = request.args.get('order', 'desc')
	orderCond = """ORDER BY user.name {}""".format(order) 

	query = """SELECT user.id, user.email, user.name, user.username, user.isAnonymous, user.about \
		FROM user \
		JOIN post ON post.user = user.email \
		WHERE post.forum = %s {sinceId} \
		GROUP BY user.id {order} {limit};""".format(
		sinceId=sinceIdCond, limit=limitCond, order=orderCond)
	data = (forum,)

	rows = executeQueryData(query,data)

	users = list()
	for row in rows:
		user = dict()
		user['id'] = row[0]
		user['email'] = row[1]
		user['name'] = row[2]
		user['username'] = row[3]
		user['isAnonymous'] = row[4]
		user['about'] = row[5]
		user['followers'] = getFollowersList(user['email'])
		user['following'] = getFollowingList(user['email'])
		user['subscriptions'] = getSubscribedThreadsList(user['email'])

		users.append(user)

	return jsonify(code = 0, response = users)



@app.route('/db/api/forum/listPosts/')
def forumListPosts():
	forum = request.args.get('forum')
	if not forum:
		return jsonify(code = 3, response = 'Missing parameters')

	related = request.args.getlist('related')
	threadInRelated = False
	forumInRelated = False
	userInRelated = False

	for relatedValue in related:
		if relatedValue == 'thread':
			threadInRelated = True
		elif relatedValue == 'forum':
			forumInRelated = True
		elif relatedValue == 'user':
			userInRelated = True
		else:
			return	jsonify(code = 3, response = 'Incorrect request')

	since = request.args.get('since', '')
	limit = request.args.get('limit', -1)
	sort = request.args.get('sort', 'flat')
	order = request.args.get('order', 'desc')

	posts = getPostList(forum=forum, since=since, limit=limit, sort=sort, order=order)

	for post in posts:
		if userInRelated:
			post['user'] = getUserDict(post['user'])

		if threadInRelated:
			post['thread'] = getThreads(threadId = post['thread'])[0]

		if forumInRelated:
			post['forum'] = getForumDict(post['forum'])

	return jsonify(code = 0, response = posts)