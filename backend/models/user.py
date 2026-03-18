"""
models/user.py
User model: stores credentials and links to Transactions.
Password is stored as a bcrypt hash — never plaintext.
"""

import bcrypt
from db import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False, default="")
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # One-to-many: a user has many transactions
    transactions = db.relationship(
        "Transaction", back_populates="user", cascade="all, delete-orphan"
    )

    # ------------------------------------------------------------------
    # Password helpers
    # ------------------------------------------------------------------

    def set_password(self, plaintext: str) -> None:
        """Hash and store a plaintext password."""
        self.password_hash = bcrypt.hashpw(
            plaintext.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

    def check_password(self, plaintext: str) -> bool:
        """Return True if the plaintext matches the stored hash."""
        return bcrypt.checkpw(
            plaintext.encode("utf-8"),
            self.password_hash.encode("utf-8"),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email}>"
