import json
import os
import tempfile
import unittest

import dashboard
from dashboard import database

class TestBase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.filename = tempfile.mkstemp()
        dashboard.app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+self.filename
        dashboard.app.config['TESTING'] = True
        self.app = dashboard.app.test_client()
        
        database.init_db()

    def tearDown(self):
        os.close(self.db_fd)

    
    def assertResponse(self, path, expected):
        resp = self.app.get(path)
        self.assertEqual(200, resp.status_code)
        print resp.data
        js = json.loads(resp.data)
        self.assertEqual(js, expected)

class TestApiBase(TestBase):

    def get(self, url, expected):
        pass

    def post(self, url, expected, status_code=302):
        pass

class TestRoutes(TestBase):
    def test_db(self):
        db = database.connect_db()
        db.execute('select * from runs').fetchall()

    def test_index(self):
        resp = self.app.get('/')
        self.assertEquals("Hello World!", resp.data)

    def test_api_monitor_index_empty(self):
        expected = {"monitors":[]}
        self.assertResponse('/api/monitor/', expected)

    def test_api_monitor_index_post(self):
        monitor = dict(name="test", url="http://test.com", interval=10)
        resp = self.app.post('/api/monitor/', content_type="application/json", data=json.dumps(monitor))
        self.assertEqual(resp.status_code, 302)


        monitor['id'] = 1
        expected = {"monitors":[monitor]}

        self.assertResponse('/api/monitor/', expected)


    def test_api_monitor(self):
        monitor = dict(name="test", url="http://test.com", interval=10)
        resp = self.app.post('/api/monitor/', content_type="application/json", data=json.dumps(monitor))
        self.assertEqual(resp.status_code, 302)

        expected = dict(data='ok') 
        self.assertResponse('/api/monitor/1', expected)
