from flask import Blueprint, request, jsonify, json
from . import db
from .models import Appointment

Appointment_blueprint = Appointment('Appointment_blueprint', __name__)
