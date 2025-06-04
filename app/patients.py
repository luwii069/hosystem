from flask import Blueprint, request, jsonify, json
from . import db
from .models import User

User_blueprint = User('User_blueprint', __name__)
