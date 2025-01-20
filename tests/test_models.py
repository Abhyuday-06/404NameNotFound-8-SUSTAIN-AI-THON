import unittest
from app import create_app, db
from models import User

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        with self.app.app_context():
            user = User(email="test@example.com", password="password123")
            db.session.add(user)
            db.session.commit()

            self.assertEqual(User.query.count(), 1)
            self.assertEqual(User.query.first().email, "test@example.com")
