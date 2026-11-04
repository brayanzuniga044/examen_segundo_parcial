from flask import Blueprint

bp_pacientes = Blueprint("pacientes", __name__)

from app.pacientes import routes
