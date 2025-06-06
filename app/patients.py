from flask import Blueprint, request, jsonify
from . import db, bcrypt
from .models import User
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
)

User_blueprint = Blueprint('User_blueprint', __name__)
#get a specific patient 
@User_blueprint.route("/search-patients", methods=["GET"])
@jwt_required()
def search_patients():
    admn_no = request.args.get('admn_no')
    
    if not admn_no:
        return jsonify({'message': "Admission number is required"}), 400

    # Search for patients matching the admn_no (case-insensitive, partial match)
    patients = User.query.filter(User.admn_no.ilike(f"%{admn_no}%")).all()
    
    if not patients:
        return jsonify({'message': "No patients found"}), 404

    return jsonify({
        'patients': [p.details() for p in patients],
        'count': len(patients)
    }), 200

# Get all patients
@User_blueprint.route("/patients", methods=["GET"])
@jwt_required()
def get_all_patients():
    patients = User.query.all()
    if not patients:
        return jsonify({'message': "No patients found"}), 404

    return jsonify({'patients': [p.details() for p in patients]}), 200

#delete a patient
@User_blueprint.route("/patients/<string:admn_no>", methods=["DELETE"])
@jwt_required()
def delete_patient_by_admn_no(admn_no):
    patient = User.query.filter_by(admn_no=admn_no).first()
    
    if not patient:
        return jsonify({'message': "Patient not found"}), 404

    db.session.delete(patient)
    db.session.commit()
    
    return jsonify({'message': "Patient deleted successfully"}), 200


# Edit patient details(still under review though)
@User_blueprint.route("/patients/<int:id>", methods=["PUT"])
@jwt_required()
def update_patient(id):
    patient = User.query.get(id)
    if not patient or patient.role != 'patient':
        return jsonify({'message': "Patient not found"}), 404

    data = request.get_json()
    patient.name = data.get("name", patient.name)
    patient.email = data.get("email", patient.email)
    patient.admn_no = data.get("admn_no", patient.admn_no)

    if data.get("password"):
        patient.password = bcrypt.generate_password_hash(data.get("password")).decode('utf-8')

    db.session.commit()
    return jsonify({'message': "Patient updated successfully", 'patient': patient.details()}), 200
