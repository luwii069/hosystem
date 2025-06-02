from . import db 
from datetime import datetime 

class Admin (db.model):
    __tablename__="admins"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # should be hashed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Admin('{self.username}')"

class Patient(db.model):
    __tablename__ ="patients"  
     
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
 

