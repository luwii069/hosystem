from flask import Blueprint, request, jsonify
from . import db, bcrypt
from .models import User
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
)

User_blueprint = Blueprint('User_blueprint', __name__)

#search patients
@User_blueprint.route("/search-patients", methods=["GET"])
@jwt_required()
def search_patients():
    admn_no = request.args.get('admn_no')
    if not admn_no:
        return jsonify({'message': "Admission number is required"}), 400

    patients = User.query.filter(User.admn_no.ilike(f"%{admn_no}%")).all()
    if not patients:
        return jsonify({'message': "No patients found"}), 404

    return jsonify({'patients': [p.details() for p in patients]}), 200

@User_blueprint.route("/patients", methods=["GET"])
@jwt_required()
def get_all_patients():
    patients = User.query.all()
    if not patients:
        return jsonify({'message': "No patients found"}), 404

    return jsonify({'patients': [p.details() for p in patients]}), 200
