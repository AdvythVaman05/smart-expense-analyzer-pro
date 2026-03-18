"""
db.py
Central SQLAlchemy instance + DB initialisation helper.
Import `db` wherever you need to define models or run queries.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    """Bind SQLAlchemy to the app and create all tables."""
    db.init_app(app)
    with app.app_context():
        # Import models so SQLAlchemy is aware of them before create_all
        from models.user import User          # noqa: F401
        from models.transaction import Transaction  # noqa: F401
        db.create_all()
