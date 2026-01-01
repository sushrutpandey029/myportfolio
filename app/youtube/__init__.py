from flask import Blueprint

youtube = Blueprint('youtube', __name__)

from app.youtube import routes