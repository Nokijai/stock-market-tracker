from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.holding import Holding
from app.schemas.portfolio import HoldingCreate, HoldingUpdate, HoldingOut, PortfolioSummary
from app.utils.auth import get_current_user
from app.services.price_service import fetch_quote, fetch_quotes_bulk
from app.services.analytics import enrich_holding, compute_portfolio_summary

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])


def _build_holding_dict(h: Holding) -> dict:
    return {
        "id": h.id, "ticker": h.ticker, "shares": h.shares,
        "avg_cost": h.avg_cost, "currency": h.currency, "added_at": h.added_at,
    }


@router.get("/", response_model=List[HoldingOut])
def list_holdings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()
    if not holdings:
        return []
    # Bulk-fetch all quotes in one shot to avoid N+1 yfinance calls
    tickers = list({h.ticker for h in holdings})
    quotes = fetch_quotes_bulk(tickers)
    return [enrich_holding(_build_holding_dict(h), quotes.get(h.ticker)) for h in holdings]


@router.get("/summary", response_model=PortfolioSummary)
def portfolio_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()
    if not holdings:
        return {
            "total_cost_basis": 0, "total_market_value": 0,
            "total_unrealized_pnl": 0, "total_return_pct": 0,
            "holdings_count": 0,
        }
    tickers = list({h.ticker for h in holdings})
    quotes = fetch_quotes_bulk(tickers)
    enriched = [enrich_holding(_build_holding_dict(h), quotes.get(h.ticker)) for h in holdings]
    return compute_portfolio_summary(enriched)


@router.post("/", response_model=HoldingOut, status_code=201)
def add_holding(payload: HoldingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticker = payload.ticker  # already validated and uppercased by schema
    existing = db.query(Holding).filter(Holding.user_id == current_user.id, Holding.ticker == ticker).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"{ticker} already in portfolio. Use PUT to update.")
    holding = Holding(user_id=current_user.id, ticker=ticker, shares=payload.shares,
                      avg_cost=payload.avg_cost, currency=payload.currency)
    db.add(holding)
    db.commit()
    db.refresh(holding)
    quote = fetch_quote(ticker)
    return enrich_holding(_build_holding_dict(holding), quote)


@router.put("/{holding_id}", response_model=HoldingOut)
def update_holding(holding_id: int, payload: HoldingUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    holding = db.query(Holding).filter(Holding.id == holding_id, Holding.user_id == current_user.id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    if payload.shares is not None:
        holding.shares = payload.shares
    if payload.avg_cost is not None:
        holding.avg_cost = payload.avg_cost
    db.commit()
    db.refresh(holding)
    quote = fetch_quote(holding.ticker)
    return enrich_holding(_build_holding_dict(holding), quote)


@router.delete("/{holding_id}", status_code=204)
def delete_holding(holding_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    holding = db.query(Holding).filter(Holding.id == holding_id, Holding.user_id == current_user.id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    db.delete(holding)
    db.commit()
