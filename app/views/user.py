from app import app
from flask import g, request, jsonify
import json
from utils import *

from MySQLdb import IntegrityError
#from sqlalchemy.exc import IntegrityError

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
		return	jsonify(code = 3, response = 'Missing parameters')
	
	try:
		query = "INSERT INTO user (name, about, username, email, isAnonymous) \
				 VALUES (%s, %s, %s, %s, %s)" 
		data = (name, about, username, email, int(isAnonymous)) 
		cur = executeQueryData(query, data)
	except IntegrityError: 
		return jsonify(code = 5, response = 'User exists')

	response = {
		'id' : cur.lastrowid,	
		'name' : name, 
		'about' : about, 
		'username' : username,
		'email' : email,
		'isAnonymous' : isAnonymous
	}

	return	jsonify(code = 0, response = response)

@app.route('/db/api/user/details/', methods=['GET'])
def userDetails(): 	
	try:		
		user = request.args.get('user')
	except KeyError:
		return	jsonify(code = 3, response = 'User not specified')

	response = getUserDict(user)
	if response == 'Not Found':
		return jsonify(code = 1, response = response)

	response['followers'] = getFollowersList(user)
	response['following'] = getFollowingList(user)
	response['subscriptions'] = getSubscribedThreadsList(user)

	return	jsonify(code = 0, response = response)


@app.route('/db/api/user/listPosts/', methods=['GET'])
def userListPosts():
	user = request.args.get('user')
	if not user:
		return jsonify(code = 3, response = 'Missing parameters')

	since = request.args.get('since', '')
	limit = request.args.get('limit', -1)
	order = request.args.get('order', 'desc')

	posts = getPostList(user=user, since=since, limit=limit, order=order)
	return jsonify(code = 0, response = posts)


@app.route('/db/api/user/updateProfile/', methods=['POST'])
def userUpdateProfile():
	dataJSON = request.get_json()
	try:
		about = dataJSON['about']
		name = dataJSON['name']
		email = dataJSON['user']
	except KeyError:
		return jsonify(code = 0, response = 'Missing parameters')

	query = "UPDATE user SET about = %s, name = %s WHERE email = %s;"
	data = (about, name, email)
	executeQueryData(query,data)

	response = getUserDict(email)

	return jsonify(code = 0, response = response)


@app.route('/db/api/user/follow/', methods=['POST'])
def userFollow():	
	dataJSON = request.get_json()
	try:
		follower = dataJSON['follower']
		followee = dataJSON['followee']
	except KeyError:
		return jsonify(code = 3, response = "Missing parameters")

	query = "INSERT INTO follower (follower, following) VALUES (%s, %s);"
	data = (follower, followee)
	executeQueryData(query,data)

	response = getUserDict(follower)

	return jsonify(code = 0, response = response)
	

@app.route('/db/api/user/unfollow/', methods=['POST'])
def userUnfollow():	
	dataJSON = request.get_json()
	try:
		follower = dataJSON['follower']
		followee = dataJSON['followee']
	except KeyError:
		return jsonify(code = 3, response = "Missing parameters")

	query = "DELETE FROM follower WHERE follower = %s AND following = %s;"
	data = (follower, followee)
	executeQueryData(query,data)

	response = getUserDict(follower)

	return jsonify(code = 0, response = response)


@app.route('/db/api/user/listFollowers/', methods=['GET'])
def userListFollowers():
	return userListFollows('followers')


@app.route('/db/api/user/listFollowing/', methods=['GET'])
def userListFollowing():
	return userListFollows('following')


def userListFollows(requestType):
	email = request.args.get('user')
	if not email:
		return jsonify(code = 3, response = 'Missing parameters')

	sinceId = request.args.get('since_id', -1)
	if sinceId != -1:
		sinceIdCond = "AND user.Id >= %s" % (sinceId)
	else:
		sinceIdCond = ""

	orderCond = "ORDER BY user.name %s" % (request.args.get('order', 'desc'))

	limit = request.args.get('limit', -1)
	if limit != -1:
		limitCond = "LIMIT {}".format( int(limit) )
	else:
		limitCond = ""

	query = "SELECT about, email, id, isAnonymous, name, username FROM user JOIN follower ON "
	if requestType == 'followers':
		query += "follower.follower = user.email WHERE follower.following"
	else:
		query += "follower.following = user.email WHERE follower.follower"

	query += " = %s {since} {order} {limit};".format(
		since=sinceIdCond, order=orderCond, limit=limitCond)

	data = (email,)
	rows = executeQueryData(query, data)
	if not rows:
		return jsonify(code = 1, response = 'Empty set')

	users = list()
	for row in rows:
		user = dict()
		user['about'] = row[0]
		user['email'] = row[1]
		user['id'] = row[2]
		user['isAnonymous'] = row[3]
		user['name'] = row[4]
		user['username'] = row[5]
		user['followers'] = getFollowersList(user['email'])
		user['following'] = getFollowingList(user['email'])
		user['subscriptions'] = getSubscribedThreadsList(user['email'])

		users.append(user)

	return jsonify(code = 0, response = users)