"""
services/anomaly_detector.py
Detects anomalous transactions using scikit-learn's Isolation Forest.

Strategy:
  - Features: amount, day-of-week, day-of-month
  - contamination=0.05 (flag ~5% of transactions as anomalies)
  - Falls back gracefully when there are too few samples
"""

import numpy as np
from typing import List, Dict, Any
from sklearn.ensemble import IsolationForest
import datetime


_MIN_SAMPLES_FOR_ML = 5  # need at least this many rows to train a model


def _extract_features(transactions: List[Dict[str, Any]]) -> np.ndarray:
    """
    Build a float feature matrix from the transaction list.
    Columns:  [amount, day_of_week (0-6), day_of_month (1-31)]
    """
    rows = []
    for tx in transactions:
        amount = float(tx.get("amount", 0))
        try:
            dt = datetime.datetime.strptime(tx["date"], "%Y-%m-%d")
            dow = dt.weekday()    # 0=Monday … 6=Sunday
            dom = dt.day          # 1-31
        except (KeyError, ValueError):
            dow, dom = 0, 1
        rows.append([amount, dow, dom])
    return np.array(rows, dtype=float)


def detect_anomalies(
    transactions: List[Dict[str, Any]],
    contamination: float = 0.05,
) -> List[Dict[str, Any]]:
    """
    Return the transaction list with an 'anomaly' boolean and 'anomaly_score'
    (lower score = more anomalous) added to each dict.
    """
    if len(transactions) < _MIN_SAMPLES_FOR_ML:
        # Not enough data — mark everything as normal
        for tx in transactions:
            tx["anomaly"] = False
            tx["anomaly_score"] = 0.0
        return transactions

    X = _extract_features(transactions)

    # contamination must be (0, 0.5]
    safe_contamination = max(0.01, min(contamination, 0.5))

    model = IsolationForest(
        n_estimators=100,
        contamination=safe_contamination,
        random_state=42,
    )
    labels = model.fit_predict(X)          # 1 = normal, -1 = anomaly
    scores = model.score_samples(X)        # lower = more anomalous

    for tx, label, score in zip(transactions, labels, scores):
        tx["anomaly"] = bool(label == -1)
        tx["anomaly_score"] = round(float(score), 4)

    return transactions


def build_alert_message(transactions: List[Dict[str, Any]]) -> str:
    """Return a human-readable alert string based on anomaly count."""
    anomaly_count = sum(1 for tx in transactions if tx.get("anomaly"))
    total = len(transactions)
    if anomaly_count == 0:
        return "✅ No anomalies detected. Your spending looks normal."
    pct = round(anomaly_count / total * 100, 1)
    return (
        f"⚠️ {anomaly_count} anomalous transaction(s) detected "
        f"({pct}% of {total} total). Please review these carefully."
    )
