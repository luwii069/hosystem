from flask import Blueprint, request, jsonify, json
from . import db
from .models import Appointment
from flask_jwt_extended import jwt_required
from datetime import datetime

Appointment_blueprint = Blueprint('Appointment_blueprint', __name__)




#creating appointments 
@Appointment_blueprint.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()

    doctor_id = data.get("doctor_id")
    patient_id = data.get("patient_id")
    date = data.get("date")
    reason = data.get("reason")

    if not all([doctor_id, patient_id, date]):
        return jsonify({"message": "doctor_id, patient_id, and date are required"}), 400

    try:
        date_obj = datetime.fromisoformat(date)
    except ValueError:
        return jsonify({"message": "Invalid date format. Use ISO format: YYYY-MM-DDTHH:MM:SS"}), 400

    appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient_id,
        date=date_obj,
        reason=reason
    )
    db.session.add(appointment)
    db.session.commit()

    return jsonify({"message": "Appointment created"}), 201

#getting all appointments 
@Appointment_blueprint.route('/appointments', methods=['GET'])
@jwt_required()
def get_all_appointments():
    appointments = Appointment.query.all()
    output = []
    for appt in appointments:
        output.append({
            "id": appt.id,
            "doctor_id": appt.doctor_id,
            "patient_id": appt.patient_id,
            "date": appt.date,
            "reason": appt.reason
        })
    return jsonify(output), 200

#getting specific appointments 
@Appointment_blueprint.route('/appointments/<int:id>', methods=['GET'])
@jwt_required()
def get_appointment(id):
    appt = Appointment.query.get(id)
    if not appt:
        return jsonify({"message": "Appointment not found"}), 404

    return jsonify({
        "id": appt.id,
        "doctor_id": appt.doctor_id,
        "patient_id": appt.patient_id,
        "date": appt.date,
        "reason": appt.reason
    }), 200

#editing appointments 
@Appointment_blueprint.route('/appointments/<int:id>', methods=['PUT'])
@jwt_required()
def update_appointment(id):
    appt = Appointment.query.get(id)
    if not appt:
        return jsonify({"message": "Appointment not found"}), 404

    data = request.get_json()
    if "date" in data:
        try:
            appt.date = datetime.fromisoformat(data["date"])
        except ValueError:
            return jsonify({"message": "Invalid date format"}), 400
    appt.reason = data.get("reason", appt.reason)

    db.session.commit()
    return jsonify({"message": "Appointment updated"}), 200

#deleting apointments
@Appointment_blueprint.route('/appointments/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(id):
    appt = Appointment.query.get(id)
    if not appt:
        return jsonify({"message": "Appointment not found"}), 404

    db.session.delete(appt)
    db.session.commit()
    return jsonify({"message": "Appointment deleted"}), 200

