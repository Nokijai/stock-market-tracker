from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.watchlist import WatchlistItem
from app.schemas.portfolio import WatchlistItemCreate, WatchlistItemOut
from app.utils.auth import get_current_user
from app.services.price_service import fetch_quote

router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])

@router.get("/", response_model=List[WatchlistItemOut])
def list_watchlist(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    items = db.query(WatchlistItem).filter(WatchlistItem.user_id == current_user.id).all()
    result = []
    for item in items:
        quote = fetch_quote(item.ticker)
        result.append({
            "id": item.id, "ticker": item.ticker, "added_at": item.added_at,
            "current_price": quote.get("price") if quote else None,
            "day_change_pct": quote.get("day_change_pct") if quote else None,
            "company_name": quote.get("company_name") if quote else None,
        })
    return result

@router.post("/", response_model=WatchlistItemOut, status_code=201)
def add_to_watchlist(payload: WatchlistItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticker = payload.ticker.upper().strip()
    existing = db.query(WatchlistItem).filter(WatchlistItem.user_id == current_user.id, WatchlistItem.ticker == ticker).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"{ticker} already in watchlist")
    item = WatchlistItem(user_id=current_user.id, ticker=ticker)
    db.add(item)
    db.commit()
    db.refresh(item)
    quote = fetch_quote(ticker)
    return {
        "id": item.id, "ticker": item.ticker, "added_at": item.added_at,
        "current_price": quote.get("price") if quote else None,
        "day_change_pct": quote.get("day_change_pct") if quote else None,
        "company_name": quote.get("company_name") if quote else None,
    }

@router.delete("/{ticker}", status_code=204)
def remove_from_watchlist(ticker: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    item = db.query(WatchlistItem).filter(WatchlistItem.user_id == current_user.id, WatchlistItem.ticker == ticker.upper()).first()
    if not item:
        raise HTTPException(status_code=404, detail="Ticker not in watchlist")
    db.delete(item)
    db.commit()
