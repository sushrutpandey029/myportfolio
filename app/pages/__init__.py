from flask import Blueprint

pages = Blueprint('pages', __name__)

from app.pages import routes