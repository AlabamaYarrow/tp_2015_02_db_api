from flask import Flask, g
import MySQLdb
import settings

app = Flask(__name__)	

@app.before_request
def db_connect():
	g.db_conn = \
	MySQLdb.connect(host=settings.DB_HOST, 
					user=settings.DB_USER, 
					passwd=settings.DB_PASSWD, 
					db=settings.DB_NAME)    
	g.db_conn.set_character_set('utf8')
	cur = g.db_conn.cursor()
	#cur.execute('SET NAMES utf8;') 
	#cur.execute('SET CHARACTER SET utf8;')
	#cur.execute('SET character_set_connection=utf8;')
	



@app.teardown_request
def db_disconnect(exception=None):
    g.db_conn.close()

from app.views import *
