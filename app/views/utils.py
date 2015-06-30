from flask import g
from app import app


def executeQuery(query):
        conn = app.db_engine.connect()
        result = conn.execute(query)
        conn.close()
        return result


def executeQueryData(query, data):
        conn = app.db_engine.connect()
        result = conn.execute(query, data)
        conn.close()
        return result


def getFollowersList(email):
	query = "SELECT follower \
			FROM follower \
			WHERE following = %s;"
	data = (email,)
	rows = executeQueryData(query, data).fetchall()
	if not rows:
		return list()
	followslist = list()
	for row in rows[0]:
		followslist.append(row)

	return followslist


def getFollowingList(email):
	query = "SELECT following \
			FROM follower \
			WHERE follower = %s;"
	data = (email,)
	rows = executeQueryData(query, data).fetchall()
	if not rows:
	    return list()
	followslist = list()
	for row in rows[0]:
		followslist.append(row)
	
	return followslist


def getPostList(user='', forum='', thread='', postId='', since='', limit=-1, \
				sort='flat', order='desc', date=''):
	if postId != "":
		whereCond = " id = %s" % (postId)
	elif forum != "":
		whereCond = " forum = '%s'" % (forum)
	elif thread != "":
		whereCond = " thread = %s" % (thread)
	elif user != "":
		if date != "":
			whereCond = " user = '%s' AND date = '%s'" % (user, date)
		else:
			whereCond = " user = '%s'" % (user)

	sinceCond = ""
	if since != "":
		sinceCond = " AND date >= '%s'" % (since)

	sortCond = ""

	limitCond = ""
	if limit != -1:			
		limitCond = " LIMIT %s" % ( int(limit) )
	
	orderCond = " ORDER BY date %s" % (order)
	
	query = "SELECT id, user, thread, forum, message, \
			parent, date, likes, dislikes, points, \
			isSpam, isEdited, isDeleted, isHighlighted, isApproved \
			FROM post \
			WHERE %s %s %s %s %s;" \
			% (whereCond, sinceCond, orderCond, sortCond, limitCond)
	rows = executeQuery(query)
	
	if not rows:
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


def getThreadList(threadId = "", title = "", forum = "", user = "", \
					since = "", limit = -1, order = "desc"):
	if threadId != "":
		whereCond = "id = %s" % (threadId)
	elif title != "":
		whereCond = "title = '%s'" % (title)
	elif forum != "":
		whereCond = "forum = '%s'" % (forum)
	elif user != "":
		whereCond = "user = '%s'" % (user)
		
	sinceCond = ""
	if since != "":
		sinceCond = "AND date >= '%s'" % (since)

	orderCond = "ORDER BY date %s" % (order)

	limitCond = ""
	if limit != -1:
		limitCond = "LIMIT %s" % ( int(limit) )

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


def getForumDict(forum):
	query = "SELECT id,name,short_name,user \
			 FROM forum \
			 WHERE short_name = %s" 
	data = (forum,)
	row = executeQueryData(query,data).fetchone()
	if not row:
		return {}
	return {
		'id' : row[0],	
		'name' : row[1], 
		'short_name' : row[2], 
		'user' : row[3]
	}	
	

def postsInThreadIncrement(threadId):
	query = "UPDATE thread SET posts = posts + 1 WHERE id = %s;"
	data = (threadId,)
	executeQueryData(query, data)


def postsInThreadDecrement(threadId):
	query = "UPDATE thread SET posts = posts - 1 WHERE id = %s;"
	data = (threadId,)
	executeQueryData(query, data)


def getSubscribedThreadsList(user):
	query = "SELECT thread FROM subscription WHERE subscriber = %s;"
	data = (user,)
	rows = executeQueryData(query, data)
	threads = list()
	for row in rows:
		threads.append(row[0])

	return threads
