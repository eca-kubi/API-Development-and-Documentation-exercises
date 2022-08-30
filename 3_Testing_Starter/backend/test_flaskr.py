import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            "student", "student", "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # @TODO: Write at least two tests for each endpoint - one each for success and error behavior.
    #        You can feel free to write additional tests for nuanced functionality,
    #        Such as adding a book without a rating, etc.
    #        Since there are four routes currently, you should have at least eight tests.
    # Optional: Update the book information in setUp to make the test database your own!
    def test_get_books(self):
        res = self.app.test_client().get('/books')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

    def test_404_invalid_page_number(self):
        res = self.app.test_client().get('/books?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertTrue(data['message'])

    def test_create_book_using_post(self):
        res = self.app.test_client().post('/books', json={"title": "a stitch in time saves nine", "author": "clinton", "rating": 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_books'])
        self.assertTrue(len(data['books']))

    def test_create_book_using_put_method(self):
        """ Put method is not allowed for creating a resource, 405 error is expected"""
        res = self.app.test_client().put('/books', json={"title": "a stitch in time saves nine", "author": "clinton", "rating": 1})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertTrue(data['message'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
