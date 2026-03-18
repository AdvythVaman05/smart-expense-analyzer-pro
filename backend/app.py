"""
Smart Expense Analyzer PRO — Flask App Factory (Phase 2)
"""

import os
from datetime import timedelta
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from db import init_db
from routes.upload import upload_bp
from routes.auth import auth_bp


def create_app():
    app = Flask(__name__)

    # ── Configuration ────────────────────────────────────────────────────────
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app.config.update(
        # Database
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL",
            f"sqlite:///{os.path.join(base_dir, 'expense_analyzer.db')}",
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        # JWT
        JWT_SECRET_KEY=os.environ.get(
            "JWT_SECRET_KEY", "0041d8462974e9871e415986b9722abc5a0b9a524bbb20d075c684d860202319"
        ),
        JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=12),

        # Upload size limit
        MAX_CONTENT_LENGTH=16 * 1024 * 1024,  # 16 MB
    )

    # ── Extensions ───────────────────────────────────────────────────────────
    CORS(app, resources={r"/*": {"origins": "*"}})
    JWTManager(app)
    init_db(app)

    # ── Blueprints ───────────────────────────────────────────────────────────
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)

    # ── Health check ─────────────────────────────────────────────────────────
    @app.route("/health")
    def health():
        return {"status": "ok", "service": "Smart Expense Analyzer API v2"}, 200

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
