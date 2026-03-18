"""
models/transaction.py
Transaction model: stores individual expense rows linked to a user.
"""

from db import db
from datetime import datetime, timezone


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    date = db.Column(db.String(10), nullable=False)          # "YYYY-MM-DD"
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, default="N/A")
    category = db.Column(db.String(60), default="Other")
    is_anomaly = db.Column(db.Boolean, default=False)
    anomaly_score = db.Column(db.Float, default=0.0)
    upload_batch = db.Column(db.String(36), nullable=True)   # UUID of the upload
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = db.relationship("User", back_populates="transactions")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "description": self.description,
            "category": self.category,
            "is_anomaly": self.is_anomaly,
            "anomaly_score": self.anomaly_score,
            "upload_batch": self.upload_batch,
        }

    def __repr__(self) -> str:
        return f"<Transaction id={self.id} amount={self.amount} category={self.category}>"
