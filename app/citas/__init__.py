from flask import Blueprint

bp_citas = Blueprint("citas", __name__)

from app.citas import routes
