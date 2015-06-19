import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy
from flask_blog import app, db

from blog.models import *
from user.models import *

class UserTest(unittest.TestCase):

    def setUp(self):
	self.db_uri = "mysql://%s:%s@mysql:3306/" % (app.config['DB_USERNAME'], app.config['DB_PASSWORD'])
	app.config['TESTING'] = True
	app.config['WTF_CSRF_ENABLED'] = False
	app.config['BLOG_DATABASE_NAME'] = 'test_blog'
	app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
	engine = sqlalchemy.create_engine(self.db_uri)
	conn = engine.connect()
	conn.execute("commit")
	conn.execute("CREATE DATABASE %s" % app.config['BLOG_DATABASE_NAME'])
	db.create_all()
	conn.close()
	self.app = app.test_client()

    def tearDown(self):
	db.session.remove()
	engine = sqlalchemy.create_engine(self.db_uri)
	conn = engine.connect()
	conn.execute("commit")
	conn.execute("DROP DATABASE %s" % app.config['BLOG_DATABASE_NAME'])
	conn.close()

    def create_blog(self):
	return self.app.post('/setup', data=dict(
	    name='My Test Blog1',
	    fullname='Another name',
	    email='newtest@fromzero.io',
	    username='tester1',
	    password='test',
	    confirm='test'
	), follow_redirects=True)

    def login(self, username, password):
	return self.app.post('/login', data=dict(
		username=username,
		password=password
	    ), follow_redirects=True)

    def logout(self):
	return self.app.get('/logout', follow_redirects=True)

    def register_user(self, fullname, email, username, password, confirm):
	return self.app.post('/register', data=dict(
		fullname=fullname,
		email=email,
		username=username,
		password=password,
		confirm=confirm
	    ), follow_redirects=True)

    def test_create_blog(self):
	rv = self.create_blog()
	assert 'Blog created' in rv.data

    def test_login_logout(self):
	self.create_blog()
	# Normal login
	rv = self.login('tester1', 'test')
	assert 'User tester1 logged in' in rv.data
        # Normal logout
	rv = self.logout()
	assert 'User logged out' in rv.data
	# Incorrect username/user not found
	rv = self.login('nouser', 'test')
	assert "Incorrect username" in rv.data
	# Incorrect password
	rv = self.login('tester1', 'incorrectpassword')
	assert "Incorrect password" in rv.data

    def test_admin(self):
	self.create_blog()
	# Normal login
	rv = self.login('tester1', 'test')
	rv = self.app.get('/admin', follow_redirects=True)
	assert "Welcome, tester1" in rv.data
	rv = self.logout()
	# Admin page access by new user that isn't admin
	rv = self.register_user('John Doe', 'john@example.com', 'john', 'test', 'test')
	assert "Author registered!" in rv.data
	rv = self.login('john', 'test')
	assert "User john logged in" in rv.data
	rv = self.app.get('/admin', follow_redirects=True)
	assert "403 Forbidden" in rv.data

    
if __name__ == "__main__":
    unittest.main()
