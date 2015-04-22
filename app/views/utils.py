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