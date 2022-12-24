# import os
# import logging
# from flask import Flask
# from dotenv import load_dotenv

# from app.auth.auth import auth


# load_dotenv()

# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     # app.config.from_mapping(
#     #     SECRET_KEY=config.SECRET_KEY
#     #     # DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
#     # )
#     logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         # app.config.from_pyfile('config.py', silent=True)
#         logging.info("App is Running... ")
#         app.config.from_mapping(
#         SECRET_KEY=os.getenv("SECRET_KEY"),
#         SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
#         # DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
#     )
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)
#         logging.info("Test config have been loaded secussfully")

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     # a simple page that says hello
#     # @app.route('/')
#     # def hello():
#     #     return 'Hello, World!'

#     app.register_blueprint(auth)

#     return app