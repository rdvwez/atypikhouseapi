from unittest import TestCase
from app.db import db
from flask import Flask, jsonify
app = Flask(__name__, instance_relative_config=True)

class BaseTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://desir:desirPass@127.0.0.1:3306/atypikbasetestpython"
        app.config['DEBUG'] = False
        with app.app_context():
            db.init_app(app)

    def setUp(self):
        with app.app_context():
            db.create_all()
        self.app = app.test_client
        self.app_context = app.app_context

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()