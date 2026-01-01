from flask import Blueprint

study_material = Blueprint('study_material', __name__)

from app.study_material import routes