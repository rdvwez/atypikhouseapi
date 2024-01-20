import os

from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_BLOCKLIST_ENABLED = os.getenv("JWT_BLOCKLIST_ENABLED")
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refesh"]
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
APP_SECRET_KEY=os.getenv("APP_SECRET_KEY")
SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI")
MAILGUN_API_KEY=os.getenv("MAILGUN_API_KEY")
FROM_EMAIL =os.getenv("FROM_EMAIL")
MAILGUN_DOMAIN=os.getenv("MAILGUN_DOMAIN")
GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_CLIENT_SECRET =  os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
GITHUB_COSUMMER_KEY=  os.getenv("GITHUB_COSUMMER_KEY") 
GITHUB_COSUMMER_SECRET= os.getenv("GITHUB_COSUMMER_SECRET")
FACEBOOK_CONSUMMER_KEY=os.getenv("FACEBOOK_CONSUMMER_KEY")
FACEBOOK_CONSUMMER_SECRET= os.getenv("FACEBOOK_CONSUMMER_SECRET")
STRIPE_ID_API= os.getenv("STRIPE_ID_API")
STRIPE_API_PUBLIC_KEY= os.getenv("STRIPE_API_PUBLIC_KEY")
STRIPE_API_SECRET_KEY=os.getenv("STRIPE_API_SECRET_KEY")
SMPT_SERVER= os.getenv("SMPT_SERVER")
SMTP_PORT= os.getenv("SMTP_PORT")
SMTP_LOGIN= os.getenv("SMTP_LOGIN")
SMTP_PASSWORD= os.getenv("SMTP_PASSWORD")
FROM_ADDR = os.getenv("FROM_ADDR")
PROPAGATE_EXCEPTIONS=os.getenv("PROPAGATE_EXCEPTIONS")
SESSION_TYPE = os.getenv("SESSION_TYPE")
SECRET_KEY = os.getenv("SECRET_KEY")
API_TITLE = os.getenv("API_TITLE")
API_VERSION = os.getenv("API_VERSION")
OPENAPI_VERSION = os.getenv("OPENAPI_VERSION")
OPENAPI_URL_PREFIX = os.getenv("OPENAPI_URL_PREFIX")
OPENAPI_SWAGGER_UI_PATH =os.getenv("OPENAPI_SWAGGER_UI_PATH")
OPENAPI_SWAGGER_UI_URL = os.getenv("OPENAPI_SWAGGER_UI_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS")
MAX_CONTENT_LENGTH = os.getenv("MAX_CONTENT_LENGTH")

MYSQL_DATABASE= os.getenv("MYSQL_DATABASE")
MYSQL_USER= os.getenv("MYSQL_USER")
MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD")
MYSQL_ROOT_PASSWORD=os.getenv("MYSQL_ROOT_PASSWORD")

UNSPLASH_ACCESS_KEY=os.getenv("UNSPLASH_ACCESS_KEY")
UNSPLASH_API_BASED_URL=os.getenv("UNSPLASH_API_BASED_URL")

FRONT_URL=os.getenv("FRONT_URL")
