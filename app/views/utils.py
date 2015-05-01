from flask import g
import MySQLdb

def executeQuery(query):
	cur = g.db_conn.cursor()
	cur.execute(query)
	g.db_conn.commit()
	return cur

def executeQueryData(query, data):
	cur = g.db_conn.cursor()
	cur.execute(query, data)
	g.db_conn.commit()
	return cur


def getFollowersList(email):
	query = """SELECT follower FROM follower WHERE following = %s;"""
	data = (email,)

	rows = executeQueryData(query, data).fetchall()

	if not rows:
		return list()

	return rows[0]


def getFollowingList(email):
	query = """SELECT following \
				FROM follower \
				WHERE follower = %s;"""
	data = (email,)

	rows = executeQueryData(query, data).fetchall()

	if not rows:
	    return list()

	return rows[0]


def getPostList(user="", forum="", thread="", postId="", since="", limit=-1, sort='flat', \
                  order='desc', date=""):
	if postId != "":
		whereCond = " id = {}".format(postId)
	elif forum != "":
		whereCond = " forum = '{}'".format(forum)
	elif thread != "":
		whereCond = " thread = {}".format(thread)
	elif user != "":
		if date != "":
			whereCond = " user = '{userValue}' AND date = '{dateValue}'".format(userValue=user, dateValue=date)
		else:
			whereCond = " user = '{userValue}'".format(userValue=user)
	else:
		print 'No criteria'
		return list()

	sinceCond = ""
	if since != "":
		sinceCond = """ AND date >= '{}'""".format(since)

	if sort != 'flat' and sort != 'tree' and sort != 'parent_tree':
		print 'Sort param error'
		return list()
	# sortCond = """ORDER BY Post.date {}""".format(sort)
	sortCond = """"""

	limitCond = ""
	if limit != -1:
		try:
			limit = int(limit)
		except ValueError:
			print 'Limit error'
			return list()
		if limit < 0:
			print 'Limit error'
			return list()
		limitCond = """ LIMIT {}""".format(limit)

	if order != 'asc' and order != 'desc':
		return jsonify(code = 3, response = 'Wrong order value')
	orderCond = """ ORDER BY date {}""".format(order)

	'''
	query = "SELECT id, user, thread, forum, message, parent, date, likes, dislikes, points, \
		isSpam, isEdited, isDeleted, isHighlighted, isApproved \
		FROM post \
		WHERE %s %s %s %s %s;"

	data = (whereCond, sinceCond, orderCond, sortCond, limitCond)
	data = (whereCond, sinceCond, orderCond, sortCond, limitCond)
	rows = executeQueryData(query, data)
	'''
	
	query = "SELECT id, user, thread, forum, message, parent, date, likes, dislikes, points, \
	isSpam, isEdited, isDeleted, isHighlighted, isApproved \
	FROM post \
	WHERE %s %s %s %s %s;" % (whereCond, sinceCond, orderCond, sortCond, limitCond)
	rows = executeQuery(query)
	
	if not rows:
		print 'Empty set'
		return list()

	posts = list()
	for row in rows:
		post = dict()
		post['id'] = row[0]
		post['user'] = row[1]
		post['thread'] = row[2]
		post['forum'] = row[3]
		post['message'] = row[4]
		post['parent'] = row[5]
		post['date'] = row[6].strftime('%Y-%m-%d %H:%M:%S')
		post['likes'] = row[7]
		post['dislikes'] = row[8]
		post['points'] = row[9]
		post['isSpam'] = row[10]
		post['isEdited'] = row[11]
		post['isDeleted'] = row[12]
		post['isHighlighted'] = row[13]
		post['isApproved'] = row[14]

		posts.append(post)

	return posts


def getThreads(threadId = "", title = "", forum = "", user = "", since = "", limit = -1, order = "desc"):
	if threadId != "":
		whereCond = "id = {}".format(threadId)
	elif title != "":
		whereCond = "title = '{}'".format(title)
	elif forum != "":
		whereCond = "forum = '{}'".format(forum)
	elif user != "":
		whereCond = "user = '{}'".format(user)
		return list()

	sinceCond = ""
	if since != "":
		sinceCond = """ AND date >= '{}'""".format(since)

	if order != 'asc' and order != 'desc':
		return list()
	orderCond = """ ORDER BY date {}""".format(order)

	limitCond = ""
	if limit != -1:
		try:
			limit = int(limit)
		except ValueError:
			return list()
		if limit < 0:
			return list()
		limitCond = """ LIMIT {}""".format( int(limit) )
	'''
	query = "SELECT id, title, user, message, \
			 forum, isDeleted, isClosed, date, slug, \
			 likes, dislikes, \
			 points, posts \
			 FROM thread \
			 WHERE %s %s %s %s;"
	data = (whereCond, sinceCond, orderCond, limitCond)
	rows = executeQueryData(query, data).fetchall()
	'''
	query = "SELECT id, title, user, message, \
			 forum, isDeleted, isClosed, date, slug, \
			 likes, dislikes, \
			 points, posts \
			 FROM thread \
			 WHERE %s %s %s %s;" % (whereCond, sinceCond, orderCond, limitCond)
	rows = executeQuery(query).fetchall()

	if not rows:
		return list()

	threads = list()
	for row in rows:
		thread = dict()
		thread['id'] = int(row[0])
		thread['title'] = row[1]
		thread['user'] = row[2]
		thread['message'] = row[3]
		thread['forum'] = row[4]
		thread['isDeleted'] = bool(row[5])
		thread['isClosed'] = bool(row[6])
		thread['date'] = row[7].strftime('%Y-%m-%d %H:%M:%S')
		thread['slug'] = row[8]
		thread['likes'] = row[9]
		thread['dislikes'] = row[10]
		thread['points'] = row[11]
		thread['posts'] = row[12]

		threads.append(thread)

	return threads


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


def postsInThreadIncrement(threadId):
	query = """UPDATE thread SET posts = posts + 1 WHERE id = %s;"""
	data = (threadId,)
	executeQueryData(query, data)


def postsInThreadDecrement(threadId):
	query = """UPDATE thread SET posts = posts - 1 WHERE id = %s;"""
	data = (threadId,)
	executeQueryData(query, data)


def getFollowerList(user):
	query = """SELECT follower FROM follower WHERE following = %s;"""
	data = (user,)
	rows = executeQueryData(query, data).fetchall()
	if not rows:
		return list()
	return rows[0]


def getFollowingList(user):
	query = """SELECT following FROM follower WHERE follower = %s;"""
	data = (user,)
	rows = executeQueryData(query, data).fetchall()
	if not rows:
		return list()
	return rows[0]


def getSubscribedThreadsList(user):
	query = "SELECT thread FROM subscription WHERE subscriber = %s;"
	data = (user,)
	rows = executeQueryData(query, data)
	threads = list()
	for row in rows:
		threads.append(row[0])

	return threads
