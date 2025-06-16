from flask import Blueprint, request, jsonify, json
from . import db,bcrypt
from datetime import timedelta, datetime
from .models import MedicalRecord,User,Doctor
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
)

MedicalRecord_blueprint =Blueprint('MedicalRecord_blueprint', __name__)

#create a medical record 
@MedicalRecord_blueprint.route('/medical-records', methods=['POST'])
@jwt_required()
def create_medical_record():
    data = request.get_json()

    doctor_id = data.get("doctor_id")
    patient_id = data.get("patient_id")
    diagnosis = data.get("diagnosis")
    treatment = data.get("treatment")

    if not all([doctor_id, patient_id, diagnosis, treatment]):
        return jsonify({"message": "All fields are required"}), 400

    record = MedicalRecord(
        doctor_id=doctor_id,
        patient_id=patient_id,
        diagnosis=diagnosis,
        treatment=treatment
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Medical record created successfully"}), 201

#get all medical records 
@MedicalRecord_blueprint.route('/medical-records', methods=['GET'])
@jwt_required()
def get_all_medical_records():
    records = MedicalRecord.query.all()
    output = []
    for r in records:
        output.append({
            "id": r.id,
            "doctor_id": r.doctor_id,
            "patient_id": r.patient_id,
            "diagnosis": r.diagnosis,
            "treatment": r.treatment,
            "date": r.date
        })
    return jsonify(output), 200


#get a specific medical record 
@MedicalRecord_blueprint.route('/medical-records/<int:id>', methods=['GET'])
@jwt_required()
def get_medical_record(id):
    record = MedicalRecord.query.get(id)
    if not record:
        return jsonify({"message": "Medical record not found"}), 404

    return jsonify({
        "id": record.id,
        "doctor_id": record.doctor_id,
        "patient_id": record.patient_id,
        "diagnosis": record.diagnosis,
        "treatment": record.treatment,
        "date": record.date
    }), 200

#edit a specific medical record 
@MedicalRecord_blueprint.route('/medical-records/<int:id>', methods=['PUT'])
@jwt_required()
def update_medical_record(id):
    record = MedicalRecord.query.get(id)
    if not record:
        return jsonify({"message": "Medical record not found"}), 404

    data = request.get_json()
    record.diagnosis = data.get("diagnosis", record.diagnosis)
    record.treatment = data.get("treatment", record.treatment)

    db.session.commit()
    return jsonify({"message": "Medical record updated"}), 200

#delete a specific medical record 
@MedicalRecord_blueprint.route('/medical-records/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_medical_record(id):
    record = MedicalRecord.query.get(id)
    if not record:
        return jsonify({"message": "Medical record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Medical record deleted"}), 200
