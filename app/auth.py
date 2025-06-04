
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
)
from datetime import timedelta, datetime
from . import db, bcrypt
from .models import Admin, Doctor, User

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([name, email, password, role]):
        return jsonify({'message': "Missing required fields"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf8')

    if role == 'admin':
        if Admin.query.filter_by(email=email).first():
            return jsonify({'message': "Email already used"}), 400
        user = Admin(name=name, email=email, password=hashed_password)

    elif role == 'doctor':
        specialization = data.get('specialization', '')
        if Doctor.query.filter_by(email=email).first():
            return jsonify({'message': "Email already used"}), 400
        user = Doctor(name=name, email=email, password=hashed_password, specialization=specialization)

    elif role == 'patient':
        admn_no = data.get('admn_no')

        if User.query.filter((User.email == email) | (User.admn_no == admn_no)).first():
            return jsonify({'message': "Email or admission number already used"}), 400

        # Find a doctor without a patient assigned
        free_doctor = Doctor.query.outerjoin(User).filter(User.id == None).first()
        if not free_doctor:
            return jsonify({'message': "No available doctor to assign"}), 400

        if not admn_no:
            now = datetime.utcnow().strftime("%Y%m%d%H%M%S")
            admn_no = f"ADM{now}"

        user = User(name=name, email=email, password=hashed_password, admn_no=admn_no, doctor_id=free_doctor.id)

    else:
        return jsonify({'message': "Invalid role"}), 400

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Sign up success"}), 201


@auth_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not all([email, password, role]):
        return jsonify({'message': "Required field missing"}), 400

    user = None
    if role == 'admin':
        user = Admin.query.filter_by(email=email).first()
    elif role == 'doctor':
        user = Doctor.query.filter_by(email=email).first()
    elif role == 'patient':
        admn_no = data.get('admn_no')
        if not admn_no:
            return jsonify({'message': "Admission number required for patients"}), 400
        user = User.query.filter_by(email=email, admn_no=admn_no).first()
    else:
        return jsonify({"message": "Invalid role"}), 400

    if not user or not bcrypt.check_password_hash(user.password.encode('utf-8'), password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(
        identity={"id": user.id, "name": user.name, "role": role},
        expires_delta=timedelta(hours=24)
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user": {"id": user.id, "name": user.name, "role": role}
    }), 200


@auth_blueprint.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = jsonify({"message": "Logout successful"})
    unset_jwt_cookies(response)
    return response, 200



