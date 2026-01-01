from flask import Blueprint

contact = Blueprint('contact', __name__)

from app.contact import routes