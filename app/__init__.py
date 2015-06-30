from flask import Flask, g
import MySQLdb
import settings

from sqlalchemy import create_engine

app = Flask(__name__)	
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

connect_string = "mysql://%s:%s@%s/%s?charset=utf8" % \
	(settings.DB_USER, settings.DB_PASSWD, settings.DB_HOST, settings.DB_NAME)

app.db_engine = create_engine(connect_string)

from app.views import *
