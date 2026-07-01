from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.user import User
from app.models.alert import Alert
from app.schemas.alert import AlertCreate, AlertOut
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/alerts", tags=["alerts"])

@router.get("/", response_model=List[AlertOut])
def list_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Alert).filter(Alert.user_id == current_user.id).order_by(Alert.created_at.desc()).all()

@router.post("/", response_model=AlertOut, status_code=201)
def create_alert(payload: AlertCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    VALID_TYPES = {"price_above", "price_below", "pct_change"}
    if payload.alert_type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"alert_type must be one of: {VALID_TYPES}")
    alert = Alert(
        user_id=current_user.id,
        ticker=payload.ticker.upper(),
        alert_type=payload.alert_type,
        threshold=payload.threshold,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert

@router.delete("/{alert_id}", status_code=204)
def delete_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    db.delete(alert)
    db.commit()

@router.patch("/{alert_id}/toggle", response_model=AlertOut)
def toggle_alert(alert_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alert = db.query(Alert).filter(Alert.id == alert_id, Alert.user_id == current_user.id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_active = not alert.is_active
    db.commit()
    db.refresh(alert)
    return alert
