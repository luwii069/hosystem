from flask import Blueprint, request, jsonify, json
from . import db
from .models import Doctor

Doctor_blueprint = Blueprint('Doctor_blueprint', __name__)

from flask_jwt_extended import jwt_required

#delete a specific doctor 
@Doctor_blueprint.route('/doctors/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted successfully'}), 200

#get all doctors
@Doctor_blueprint.route('/doctors', methods=['GET'])
@jwt_required()
def get_all_doctors():
    doctors = Doctor.query.all()
    doctor_list = [{
        'id': d.id,
        'name': d.name,
        'email': d.email,
        'specialization': d.specialization  # adjust fields as needed
    } for d in doctors]

    return jsonify({'doctors': doctor_list, 'count': len(doctor_list)}), 200

