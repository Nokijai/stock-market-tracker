from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.holding import Holding
from app.schemas.portfolio import HoldingCreate, HoldingUpdate, HoldingOut, PortfolioSummary
from app.utils.auth import get_current_user
from app.services.price_service import fetch_quote
from app.services.analytics import enrich_holding, compute_portfolio_summary

router = APIRouter(prefix="/api/portfolio", tags=["portfolio"])

@router.get("/", response_model=List[HoldingOut])
def list_holdings(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()
    enriched = []
    for h in holdings:
        d = {
            "id": h.id, "ticker": h.ticker, "shares": h.shares,
            "avg_cost": h.avg_cost, "currency": h.currency, "added_at": h.added_at,
        }
        quote = fetch_quote(h.ticker)
        enriched.append(enrich_holding(d, quote))
    return enriched

@router.get("/summary", response_model=PortfolioSummary)
def portfolio_summary(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    holdings = db.query(Holding).filter(Holding.user_id == current_user.id).all()
    enriched = []
    for h in holdings:
        d = {
            "id": h.id, "ticker": h.ticker, "shares": h.shares,
            "avg_cost": h.avg_cost, "currency": h.currency, "added_at": h.added_at,
        }
        quote = fetch_quote(h.ticker)
        enriched.append(enrich_holding(d, quote))
    return compute_portfolio_summary(enriched)

@router.post("/", response_model=HoldingOut, status_code=201)
def add_holding(payload: HoldingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    ticker = payload.ticker.upper().strip()
    existing = db.query(Holding).filter(Holding.user_id == current_user.id, Holding.ticker == ticker).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"{ticker} already in portfolio. Use PUT to update.")
    holding = Holding(user_id=current_user.id, ticker=ticker, shares=payload.shares,
                      avg_cost=payload.avg_cost, currency=payload.currency)
    db.add(holding)
    db.commit()
    db.refresh(holding)
    d = {"id": holding.id, "ticker": holding.ticker, "shares": holding.shares,
         "avg_cost": holding.avg_cost, "currency": holding.currency, "added_at": holding.added_at}
    quote = fetch_quote(ticker)
    return enrich_holding(d, quote)

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
    d = {"id": holding.id, "ticker": holding.ticker, "shares": holding.shares,
         "avg_cost": holding.avg_cost, "currency": holding.currency, "added_at": holding.added_at}
    quote = fetch_quote(holding.ticker)
    return enrich_holding(d, quote)

@router.delete("/{holding_id}", status_code=204)
def delete_holding(holding_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    holding = db.query(Holding).filter(Holding.id == holding_id, Holding.user_id == current_user.id).first()
    if not holding:
        raise HTTPException(status_code=404, detail="Holding not found")
    db.delete(holding)
    db.commit()
