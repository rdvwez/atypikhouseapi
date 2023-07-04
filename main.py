import os
import logging

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from app.db import db
from blocklist import BLOCKLIST
from app.libs.oa import oauth
# from fixtures import fixtures_loader
from fixtures.fixtures_loader import load_all_fixtures
from flask_uploads import configure_uploads, patch_request_class,  UploadSet, IMAGES
# import models

# from app.libs.image_helper import IMAGE_SET
from app.categories.ressources import blp as CategoryBleuprint
from app.houses.ressources import blp as HouseBleuprint
from app.users.ressources import blp as UsersBleuprint
from app.thematics.ressources import blp as ThematicBlueprint
from app.properties.ressources import blp as PropertyBlueprint
from app.values.ressources import blp as ValuesBlueprint
from app.images.ressources import blp as ImagesBlueprint
from app.sso.ressources import blp as SsoBlueprint
from app.reservations.ressources import blp as ReservationBlueprint

# from . import default_config

def create_app(db_url=None):
    app = Flask(__name__, instance_relative_config=True)

    #TODO move the load_dotenv function before calling  'oauth'
    load_dotenv(".env", verbose=True)
    app.config.from_object("default_config")
    # app.config.from_envvar("APPLICATION_SETTINGS")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    IMAGE_SET = UploadSet("images", IMAGES) 
    patch_request_class(app, 10 * 1024 * 1024) # 10 Mb max size upload
    configure_uploads(app, IMAGE_SET)

    # logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = "this-app_app-secret"
    app.config["API_TITLE"] = "Hatypik Rest api"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/api"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] =db_url or  os.getenv("DATABASE_URL","sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"] # allow blascklisting for access and refresh tokens
    app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

    db.init_app(app)

    api = Api(app)

    
    app.config["JWT_SECRET_KEY"] = os.environ.get("APP_SECRET_KEY")
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

    ####################################
    # @app.before_first_request
    # def create_tables_load_fixtures():
    #     # db.create_all()
    #     app.logger.info('Database tables has been created with success')
    #     # load_all_fixtures()
    #     app.logger.info('Fixtures have been loaded successfully')
    #################################################

    
    # initialisation des tables et chargement des données initiales
    # def init_db():
    #     with app.app_context():
    #         db.create_all()
    #         load_all_fixtures()

    # app.init_app(init_db)



    api.register_blueprint(CategoryBleuprint)
    api.register_blueprint(HouseBleuprint)
    api.register_blueprint(UsersBleuprint)
    api.register_blueprint(ThematicBlueprint)
    api.register_blueprint(PropertyBlueprint)
    api.register_blueprint(ValuesBlueprint)
    api.register_blueprint(ImagesBlueprint)
    api.register_blueprint(SsoBlueprint)
    api.register_blueprint(ReservationBlueprint)

    return app