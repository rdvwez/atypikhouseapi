from crypt import methods
from flask import Blueprint

auth = Blueprint("auth", __name__, url_prefix="/api")

@auth.post("/register")
def register():
    return "User created"

# @auth.get("/me")
# def 