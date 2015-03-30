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

@app.teardown_request
def db_disconnect(exception=None):
    g.db_conn.close()

from app import views, viewsForum
