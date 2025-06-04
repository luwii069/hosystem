from flask import Blueprint, request, jsonify, json
from . import db
from .models import MedicalRecord

MedicalRecord_blueprint =Blueprint('MedicalRecord_blueprint', __name__)
