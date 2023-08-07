from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from injector import inject
from flask_jwt_extended import jwt_required

from app.research.service import ResearchService, Research
from schemas import ResearchSchema, HouseSchema


blp = Blueprint("Research",__name__,description="research Engine", url_prefix="/api")

@blp.route("/research")
class ResearchEngin(MethodView):
    @inject
    def __init__(self):
        self.research_service = ResearchService()


    @blp.arguments(ResearchSchema)
    @blp.response(201, HouseSchema)
    # property_data contain the json wich is the validated fileds that the schamas requested
    def post(self, research_data):
        research_object = Research(**research_data)
        return self.research_service.find_available_houses(research_object)