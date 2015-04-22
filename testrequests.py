import requests
import json

##Common

urlBase = 'http://127.0.0.1:5000/db/api/'

def clear():
	url = urlBase + 'clear/'
	r = requests.post(url)
	print r.status_code
	print r.json()


def status():
	return 0

##FORUM

def forumCreate():
	url = urlBase + 'forum/create/'
	
	data = {
	'name': u'\u0424\u043e\u0440\u0443\u043c \u0422\u0440\u0438',
	'short_name': 'forumwithsufficientlylargename', 
	'user': 'richard.nixon@example.com'
	}
	
	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	
	r = requests.post(url, data=json.dumps(data), headers=headers)
	
	print r.status_code
	print r.json()	


##USER

def userCreate():
	url = urlBase + 'user/create/'
	
	data = {
	'username': 'user1', 
 	'about': 'hello im user1', 
 	'isAnonymous': False, 
 	'name': 'John', 
 	'email': 'example@mail.ru'
	}

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	r = requests.post(url, data=json.dumps(data), headers=headers)	
	print r.status_code
	print r.json()	


def userDetails():
	url = urlBase + 'user/details/'
	data = {'user': 'example@mail.ru'}
	r = requests.get(url, params=data)	
	print r.status_code
	print r.json()	


forumCreate()
clear()













