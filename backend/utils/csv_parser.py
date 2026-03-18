"""
utils/csv_parser.py
Parses and validates uploaded CSV expense files.

Expected CSV columns (flexible):
  - date      : transaction date (any common format)
  - amount    : numeric transaction amount
  - description / merchant / name : text description

Returns a list of normalised row dicts.
"""

import io
import pandas as pd
from typing import List, Dict, Any


# Synonyms we accept for each canonical column name
COLUMN_ALIASES: Dict[str, List[str]] = {
    "date": ["date", "transaction_date", "trans_date", "day"],
    "amount": ["amount", "debit", "credit", "value", "price", "cost"],
    "description": [
        "description", "desc", "merchant", "name", "narration",
        "transaction_description", "details", "note",
    ],
}


def _resolve_columns(df: pd.DataFrame) -> Dict[str, str]:
    """Return a mapping {canonical: actual_df_col} for recognised columns."""
    lower_cols = {c.lower().strip(): c for c in df.columns}
    mapping: Dict[str, str] = {}
    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in lower_cols:
                mapping[canonical] = lower_cols[alias]
                break
    return mapping


def parse_csv(file_stream: Any) -> List[Dict[str, Any]]:
    """
    Parse a CSV file stream and return a list of normalised expense dicts.

    Each dict has keys: date (str), amount (float), description (str).
    Raises ValueError with a descriptive message on invalid input.
    """
    try:
        raw = file_stream.read()
        # Support both bytes and str streams
        if isinstance(raw, bytes):
            raw = raw.decode("utf-8-sig")  # strip BOM if present
        df = pd.read_csv(io.StringIO(raw))
    except Exception as exc:
        raise ValueError(f"Could not read CSV: {exc}") from exc

    if df.empty:
        raise ValueError("The uploaded CSV file is empty.")

    col_map = _resolve_columns(df)

    missing = [k for k in ("date", "amount") if k not in col_map]
    if missing:
        raise ValueError(
            f"CSV is missing required column(s): {missing}. "
            f"Found columns: {list(df.columns)}"
        )

    # Normalise
    df = df.rename(columns={v: k for k, v in col_map.items()})

    # Parse dates
    df["date"] = pd.to_datetime(df["date"], infer_datetime_format=True, errors="coerce")
    df = df.dropna(subset=["date"])  # drop rows with unparseable dates

    # Coerce amount to float; drop non-numeric rows
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["amount"])

    # Keep only positive amounts (expenses); ignore credits/refunds
    df = df[df["amount"] > 0].copy()

    if df.empty:
        raise ValueError("No valid expense rows found after parsing.")

    # Fill missing description
    if "description" not in df.columns:
        df["description"] = "N/A"
    else:
        df["description"] = df["description"].fillna("N/A").astype(str)

    # Format date as ISO string
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    records = df[["date", "amount", "description"]].to_dict(orient="records")
    return records
