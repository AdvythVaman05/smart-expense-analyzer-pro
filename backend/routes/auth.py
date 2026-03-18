"""
routes/auth.py
POST /register  — create a new user account
POST /login     — return a JWT access token
GET  /me        — return current user profile (JWT protected)
POST /logout    — client-side; returns confirmation msg
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from db import db
from models.user import User

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ── helpers ──────────────────────────────────────────────────────────────────

def _validate_email(email: str) -> bool:
    return "@" in email and "." in email.split("@")[-1]


# ── endpoints ─────────────────────────────────────────────────────────────────

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Body (JSON):
      { "email": "...", "password": "...", "full_name": "..." }
    Returns:
      201 + { "message": "...", "user": {...} }
    """
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    full_name = (data.get("full_name") or "").strip()

    # --- Validation ---
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    if not _validate_email(email):
        return jsonify({"error": "Invalid email format."}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "An account with this email already exists."}), 409

    # --- Create user ---
    user = User(email=email, full_name=full_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Account created successfully.",
        "user": user.to_dict(),
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Body (JSON):
      { "email": "...", "password": "..." }
    Returns:
      200 + { "access_token": "...", "user": {...} }
    """
    data = request.get_json(silent=True) or {}

    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400

    user = User.query.filter_by(email=email).first()

    # Deliberately vague error to prevent user enumeration
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password."}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "access_token": access_token,
        "user": user.to_dict(),
    }), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    """Return the current authenticated user's profile."""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404
    return jsonify({"user": user.to_dict()}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    """
    Stateless JWT — the real logout happens client-side by deleting the token.
    This endpoint just confirms the action.
    """
    return jsonify({"message": "Logged out successfully. Please delete your token."}), 200
