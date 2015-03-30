from app import app
from flask import g, request, jsonify

def executeQuery(query):
	cur = g.db_conn.cursor()
	cur.execute(query)
	g.db_conn.commit()
	return cur

@app.route('/')
@app.route('/db/api', methods=['GET'])
def index():
	return 'Welcome to DB api!'

@app.route('/db/api/status')
def status():	
	query = 'SELECT \
			(SELECT COUNT(id) \
			FROM user),\
			(SELECT COUNT(id) \
			FROM thread),\
			(SELECT COUNT(id) \
			FROM forum),\
			(SELECT COUNT(id) \
			FROM post)'
						
	cur = executeQuery(query)	
	r = cur.fetchone()
	return jsonify (code = 0, 	response = dict(
								user = r[0],
								thread = r[1],
								forum = r[2],
								post = r[3]
								))

@app.route('/db/api/clear')
def clear():	
	query = 'TRUNCATE TABLE forum'
	executeQuery(query)	
	return jsonify (code = 0, response = 'OK')

