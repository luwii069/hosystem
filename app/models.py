from . import db 
from flask import json
from sqlalchemy import Numeric

from datetime import datetime

class Admin(db.Model):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    specialization = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one with User (Patient)
    patient = db.relationship("User", back_populates="doctor", uselist=False)

    # Doctor's medical records (one-to-many)
    medical_records = db.relationship("MedicalRecord", back_populates="doctor", cascade="all, delete-orphan")

    # Appointments (if needed in future)
    appointments = db.relationship("Appointment", back_populates="doctor", cascade="all, delete-orphan")


class User(db.Model):  # Patient
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    admn_no = db.Column(db.String(50), unique=True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-one link to doctor
    doctor = db.relationship("Doctor", back_populates="patient")

    # Patient's medical records (one-to-many)
    medical_records = db.relationship("MedicalRecord", back_populates="patient", cascade="all, delete-orphan")

    # Appointments (if needed in future)
    appointments = db.relationship("Appointment", back_populates="patient", cascade="all, delete-orphan")

    def details(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "admn_no": self.admn_no,
            "doctor_id": self.doctor_id
        }


class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("Doctor", back_populates="appointments")
    patient = db.relationship("User", back_populates="appointments")


class MedicalRecord(db.Model):
    __tablename__ = 'medical_records'
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    treatment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    doctor = db.relationship("Doctor", back_populates="medical_records")
    patient = db.relationship("User", back_populates="medical_records")
