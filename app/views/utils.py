from flask import g
import MySQLdb

def verifyJSON(dictionary):
	for key, value in dictionary.iteritems(): 		
		if value == 'None':
			dictionary[key] = None
	return dictionary

def executeQuery(query):
	cur = g.db_conn.cursor()
	cur.execute(query)
	g.db_conn.commit()
	return cur