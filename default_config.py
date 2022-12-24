import os

DEBUG = True
SQLALCHEMY_DATABASE_URI="mysql+pymysql://desir:desirPass@127.0.0.1:3306/atypikbasepython"
SQLALCHEMY_TRACK_MODIFICATIONS = False
PROPAGATE_EXCEPTIONS = True
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_BLOCKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refesh"]
UPLOADED_IMAGES_DEST = os.path.join("static", "images")

# API_TITLE= "Hatypik Rest api"
# OPENAPI_VERSION = "3.0.3"
# OPENAPI_URL_PREFIX = "/"
# OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
# OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
# JWT_BLOCKLIST_TOKEN_CHECKS = [
#     "access",
#     "refresh",
# ]  # allow blocklisting for access and refresh tokens
