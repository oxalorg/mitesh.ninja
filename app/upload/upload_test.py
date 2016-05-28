import json
from io import BytesIO

from app import app, db
import unittest

class UploadTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test_test.db'
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_upload_single_file(self):
        rv = self.app.post('/upload', data={'file[]': [(BytesIO(b'lol content'), 'lol1.jpeg')]}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_upload_multiple_files(self):
        rv = self.app.post('/upload', data={'file[]': [(BytesIO(b'lol content'), 'lol1.jpeg'), (BytesIO(b'123981y23987'), '123.pdf')]}, follow_redirects=True)
        self.assertEqual(rv.status_code, 200)

    def test_upload_disallowed_extension(self):
        rv = self.app.post('/upload', data={'file[]': [(BytesIO(b'lol content'), 'lol1.docx')]},
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode('utf-8'))['success'], 0)

    def test_upload_illegal_extension(self):
        rv = self.app.post('/upload', data={'file[]': [(BytesIO(b'lol content'), 'lol1.lol')]},
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode('utf-8'))['success'], 0)

    def test_upload_no_extension(self):
        rv = self.app.post('/upload', data={'file[]': [(BytesIO(b'123'), 'lollol')]},
                           follow_redirects=True)
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(json.loads(rv.data.decode('utf-8'))['success'], 0)


if __name__ == '__main__':
    unittest.main()