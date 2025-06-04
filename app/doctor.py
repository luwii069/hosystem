from flask import Blueprint, request, jsonify, json
from . import db
from .models import Doctor

Doctor_blueprint = Doctor('Doctor_blueprint', __name__)
