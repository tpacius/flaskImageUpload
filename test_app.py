from app import app
from io import BytesIO
import unittest

class appTestCase(unittest.TestCase):

	def setUp(self):
		self.app = app
		self.app.config['TESTING'] = True
		self.client = self.app.test_client()

	def tearDown(self):
		pass

	def upload_file(self, file):
		return self.client.post('/', data = {'file': (BytesIO(b'TEST'), file), }, follow_redirects=True, content_type='multipart/form-data')

	def test_uploaded_file(self):
		rv = self.upload_file("test.png")
		assert rv.status_code == 200
		rv = self.upload_file("test.pdf")
		assert rv.status_code == 200 
		rv = self.upload_file("test.jpeg")
		assert rv.status_code == 200 
		rv = self.upload_file("test.jpg")
		assert rv.status_code == 200 
		rv = self.upload_file("test.gif")
		assert rv.status_code == 200 

	def test_invalid_file(self):
		rv = self.upload_file("test.py")
		assert b'Invalid file format' in rv.data
		rv = self.upload_file("test.html")
		assert b'Invalid file format' in rv.data
		rv = self.upload_file("test.js")
		assert b'Invalid file format' in rv.data

if __name__ == '__main__':
	unittest.main()
		