import os
import logging

from flask import Flask, jsonify, render_template
from flask_smorest import Api
from flask_cors import CORS, cross_origin
# from flask_restful_swagger_3 import Api

from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from app.db import db
from blocklist import BLOCKLIST
from fixtures.fixtures_loader import load_all_fixtures
from flask_uploads import configure_uploads,  UploadSet, IMAGES
import default_config as dc

from app.categories.ressources import blp as CategoryBleuprint
from app.houses.ressources import blp as HouseBleuprint
from app.users.ressources import blp as UsersBleuprint
from app.thematics.ressources import blp as ThematicBlueprint
from app.properties.ressources import blp as PropertyBlueprint
from app.values.ressources import blp as ValuesBlueprint
from app.images.ressources import blp as ImagesBlueprint
from app.sso.ressources import blp as SsoBlueprint
from app.reservations.ressources import blp as ReservationBlueprint
from app.research.ressources import blp as ResearchBlueprint

# from . import default_config

def create_app(db_url=None):
    app = Flask(__name__, instance_relative_config=True)

    # Initialisez CORS avec votre application Flask
    CORS(app, ressources={r"/api/*":{"origins": "*"}} )

    #TODO move the load_dotenv function before calling  'oauth'
    # load_dotenv(".env", verbose=True)
    app.config.from_object("default_config")
    # app.config.from_envvar("APPLICATION_SETTINGS")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    IMAGE_SET = UploadSet("images", IMAGES) 
    # patch_request_class(app, 10 * 1024 * 1024) # 10 Mb max size upload
    configure_uploads(app, IMAGE_SET)

    # logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    app.config["PROPAGATE_EXCEPTIONS"] = dc.PROPAGATE_EXCEPTIONS
    app.config['SESSION_TYPE'] = dc.SESSION_TYPE
    app.config['SECRET_KEY'] = dc.SECRET_KEY
    app.config["API_TITLE"] = dc.API_TITLE
    app.config["API_VERSION"] = dc.API_VERSION
    app.config["OPENAPI_VERSION"] = dc.OPENAPI_VERSION
    app.config["OPENAPI_URL_PREFIX"] = dc.OPENAPI_URL_PREFIX
    app.config["OPENAPI_SWAGGER_UI_PATH"] = dc.OPENAPI_SWAGGER_UI_PATH
    app.config["OPENAPI_SWAGGER_UI_URL"] = dc.OPENAPI_SWAGGER_UI_URL
    app.config["SQLALCHEMY_DATABASE_URI"] =db_url or dc.SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = dc.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = dc.JWT_BLACKLIST_TOKEN_CHECKS # allow blascklisting for access and refresh tokens
    app.config['MAX_CONTENT_LENGTH'] = dc.MAX_CONTENT_LENGTH

    db.init_app(app)

    api = Api(app, spec_kwargs={'security': [{'Bearer Auth': []}]})

    
    app.config["JWT_SECRET_KEY"] = dc.JWT_SECRET_KEY
    jwt = JWTManager(app)

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (jsonify({"description":"The token is not fresh.", "error":"fresh token required"}))

    #TODO verify this function synthaxe
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(jsonify({"desciption": "the token has been revoked.", "error":"token revoked"}))

    @jwt.expired_token_loader
    def expired_torken_cillback(jwt_header, jwt_payload):
        return (jsonify({"message":"The token has expired.", "error": "token_expired"}), 401,)

    @jwt.invalid_token_loader
    def invalid_torken_cillback(error):
        return (jsonify({"message":"Signature verification failled.", "error": "invalid token"}), 401,)

    # has_run = False
    ####################################
    @app.before_first_request
    def create_tables_load_fixtures():
        global has_run
        # if not has_run:
        #     has_run = True
        if not db.engine.has_table('categories'):
            db.create_all()
            app.logger.info('Database tables has been created with success')
            load_all_fixtures()
            app.logger.info('Fixtures have been loaded successfully')
    #####################################



    api.register_blueprint(CategoryBleuprint)
    api.register_blueprint(HouseBleuprint)
    api.register_blueprint(UsersBleuprint)
    api.register_blueprint(ThematicBlueprint)
    api.register_blueprint(PropertyBlueprint)
    api.register_blueprint(ValuesBlueprint)
    api.register_blueprint(ImagesBlueprint)
    api.register_blueprint(SsoBlueprint)
    api.register_blueprint(ReservationBlueprint)
    api.register_blueprint(ResearchBlueprint)

    @app.route('/')
    def home():
        return render_template('home.html')

    return app