from flask import Blueprint, request, jsonify, json
from . import db
from .models import Doctor

Doctor_blueprint = Blueprint('Doctor_blueprint', __name__)

from flask_jwt_extended import jwt_required

@Doctor_blueprint.route('/doctors/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_doctor(id):
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({'message': 'Doctor not found'}), 404

    db.session.delete(doctor)
    db.session.commit()
    return jsonify({'message': 'Doctor deleted successfully'}), 200
