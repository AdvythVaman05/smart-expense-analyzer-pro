"""
routes/upload.py
POST /upload — Accepts a CSV file and returns expense analysis.
Requires a valid JWT token (Authorization: Bearer <token>).
Persists transactions to the database linked to the authenticated user.
"""

import uuid
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from db import db
from models.transaction import Transaction
from models.user import User
from utils.csv_parser import parse_csv
from utils.categorizer import (
    categorize_transactions,
    build_category_summary,
    build_monthly_summary,
)
from services.anomaly_detector import detect_anomalies, build_alert_message

upload_bp = Blueprint("upload", __name__)

ALLOWED_EXTENSIONS = {"csv"}


def _allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    """
    POST /upload (multipart/form-data, key='file')
    Header: Authorization: Bearer <access_token>

    Returns:
    {
        "transactions":     [...],
        "category_summary": {...},
        "monthly_summary":  {...},
        "anomalies":        [...],
        "alert":            "...",
        "upload_batch":     "<uuid>"
    }
    """
    # --- Auth ---
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "Authenticated user not found."}), 404

    # --- Validate file ---
    if "file" not in request.files:
        return jsonify({"error": "No file part in request. Use key 'file'."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected."}), 400

    if not _allowed_file(file.filename):
        return jsonify({"error": "Only CSV files are accepted."}), 400

    # --- Parse CSV ---
    try:
        transactions = parse_csv(file.stream)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 422

    if not transactions:
        return jsonify({"error": "CSV contained no valid transactions."}), 422

    # --- Enrich ---
    transactions = categorize_transactions(transactions)
    transactions = detect_anomalies(transactions)

    # --- Persist to DB (grouped by batch UUID) ---
    batch_id = str(uuid.uuid4())
    db_rows = []
    for tx in transactions:
        row = Transaction(
            user_id=user_id,
            date=tx["date"],
            amount=float(tx["amount"]),
            description=tx.get("description", "N/A"),
            category=tx.get("category", "Other"),
            is_anomaly=bool(tx.get("anomaly", False)),
            anomaly_score=float(tx.get("anomaly_score", 0.0)),
            upload_batch=batch_id,
        )
        db_rows.append(row)

    db.session.bulk_save_objects(db_rows)
    db.session.commit()

    # --- Build summaries ---
    category_summary = build_category_summary(transactions)
    monthly_summary = build_monthly_summary(transactions)
    anomalies = [tx for tx in transactions if tx.get("anomaly")]
    alert = build_alert_message(transactions)

    return jsonify({
        "transactions": transactions,
        "category_summary": category_summary,
        "monthly_summary": monthly_summary,
        "anomalies": anomalies,
        "alert": alert,
        "upload_batch": batch_id,
    }), 200


@upload_bp.route("/transactions", methods=["GET"])
@jwt_required()
def get_transactions():
    """
    GET /transactions — Return all transactions for the current user.
    Optional query param: ?batch=<uuid> to filter by upload batch.
    """
    user_id = int(get_jwt_identity())
    batch = request.args.get("batch")

    query = Transaction.query.filter_by(user_id=user_id)
    if batch:
        query = query.filter_by(upload_batch=batch)

    rows = query.order_by(Transaction.date.desc()).all()
    return jsonify({"transactions": [r.to_dict() for r in rows]}), 200
