from flask import Blueprint, request, jsonify, json
from . import db
from .models import Appointment

Appointment_blueprint = Blueprint('Appointment_blueprint', __name__)


