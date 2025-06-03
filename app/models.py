from . import db 
from flask import json
from sqlalchemy import Numeric
from datetime import datetime, timedelta

class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Admin('{self.username}')"

##
class User(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    admn_no = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    gender = db.Column(db.String(10))
    date_of_birth = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    created_by_admin = db.relationship('Admin', foreign_keys=[created_by_admin_id])

    appointments = db.relationship('Appointment', backref='patient', lazy=True)
    medical_records = db.relationship('MedicalRecord', backref='patient', lazy=True)

    def __repr__(self):
        return f"Patient('{self.name}', '{self.email}', '{self.admn_no}')"


class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    specialization = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    created_by_admin = db.relationship('Admin', foreign_keys=[created_by_admin_id])

    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __repr__(self):
        return f"Doctor('{self.name}', '{self.specialization}')"


class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patients.id'), nullable=False)
    doctor_id = db.Column(db.BigInteger, db.ForeignKey('doctors.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    created_by_admin = db.relationship('Admin', foreign_keys=[created_by_admin_id])

    def __repr__(self):
        return f"Appointment('{self.patient_id}', '{self.doctor_id}', '{self.appointment_time}')"


class MedicalRecord(db.Model):
    __tablename__ = "medicalrecords"
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger, db.ForeignKey('patients.id'), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=False)
    treatment = db.Column(db.Text)
    date_recorded = db.Column(db.DateTime, default=datetime.utcnow)

    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('admins.id'))
    created_by_admin = db.relationship('Admin', foreign_keys=[created_by_admin_id])

    def __repr__(self):
        return f"MedicalRecord('{self.patient_id}', '{self.diagnosis}')"

 

