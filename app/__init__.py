from flask import Flask, g
import MySQLdb
import settings

app = Flask(__name__)	
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

@app.before_request
def db_connect():
	g.db_conn = \
	MySQLdb.connect(host=settings.DB_HOST, 
					user=settings.DB_USER, 
					passwd=settings.DB_PASSWD, 
					db=settings.DB_NAME)    
	g.db_conn.set_character_set('utf8')


@app.teardown_request
def db_disconnect(exception=None):
    g.db_conn.close()

from app.views import *
