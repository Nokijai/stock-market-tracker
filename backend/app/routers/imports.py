import csv
import re
import io
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.holding import Holding
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/import", tags=["import"])

_TICKER_RE = re.compile(r"^[A-Z0-9.\-^]{1,10}$")

_VALID_CURRENCIES = {"USD", "EUR", "GBP", "JPY", "CAD", "AUD", "CHF", "CNY", "HKD", "SGD", "INR", "MXN", "BRL"}


def _validate_ticker(v: str) -> str:
    t = v.upper().strip()
    if not _TICKER_RE.match(t):
        raise ValueError(f"Invalid ticker symbol: {v!r}")
    return t


@router.post("/csv")
def import_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file must have a .csv extension",
        )

    content = file.file.read()
    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError:
        try:
            decoded = content.decode("latin-1")
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not decode file as UTF-8 or Latin-1",
            ) from exc

    reader = csv.DictReader(io.StringIO(decoded))

    # Normalise header names (lowercase, strip whitespace)
    reader.fieldnames = [h.strip().lower() if h else "" for h in reader.fieldnames]

    required = {"ticker", "shares", "avg_cost"}
    if not reader.fieldnames or not required.issubset(reader.fieldnames):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"CSV must contain columns: {', '.join(sorted(required))} (ticker,shares,avg_cost,currency optional)",
        )

    imported = 0
    skipped = 0
    errors: List[str] = []

    for row_num, row in enumerate(reader, start=2):  # header = row 1
        try:
            ticker_raw = row.get("ticker", "").strip()
            if not ticker_raw:
                skipped += 1
                errors.append(f"Row {row_num}: empty ticker")
                continue

            ticker = _validate_ticker(ticker_raw)

            shares_raw = row.get("shares", "").strip()
            if not shares_raw:
                skipped += 1
                errors.append(f"Row {row_num}: missing shares for {ticker}")
                continue
            try:
                shares = float(shares_raw)
            except ValueError:
                skipped += 1
                errors.append(f"Row {row_num}: invalid shares value {shares_raw!r} for {ticker}")
                continue
            if shares <= 0:
                skipped += 1
                errors.append(f"Row {row_num}: shares must be positive for {ticker}, got {shares}")
                continue

            cost_raw = row.get("avg_cost", "").strip()
            if not cost_raw:
                skipped += 1
                errors.append(f"Row {row_num}: missing avg_cost for {ticker}")
                continue
            try:
                avg_cost = float(cost_raw)
            except ValueError:
                skipped += 1
                errors.append(f"Row {row_num}: invalid avg_cost value {cost_raw!r} for {ticker}")
                continue
            if avg_cost <= 0:
                skipped += 1
                errors.append(f"Row {row_num}: avg_cost must be positive for {ticker}, got {avg_cost}")
                continue

            currency_raw = row.get("currency", "").strip().upper()
            currency = currency_raw if currency_raw in _VALID_CURRENCIES else "USD"

            # Upsert logic
            existing = (
                db.query(Holding)
                .filter(Holding.user_id == current_user.id, Holding.ticker == ticker)
                .first()
            )

            if existing:
                # Weighted average cost
                old_shares = existing.shares
                old_avg_cost = existing.avg_cost
                new_shares = old_shares + shares
                new_avg_cost = (old_shares * old_avg_cost + shares * avg_cost) / new_shares
                existing.shares = new_shares
                existing.avg_cost = new_avg_cost
                existing.currency = currency
            else:
                holding = Holding(
                    user_id=current_user.id,
                    ticker=ticker,
                    shares=shares,
                    avg_cost=avg_cost,
                    currency=currency,
                )
                db.add(holding)

            imported += 1

        except ValueError as exc:
            skipped += 1
            errors.append(f"Row {row_num}: {exc}")
        except Exception as exc:
            skipped += 1
            errors.append(f"Row {row_num}: unexpected error: {exc}")

    db.commit()

    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors,
    }