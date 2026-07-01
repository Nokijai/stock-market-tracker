from typing import List, Dict, Optional
from app.services.price_service import fetch_quote

def enrich_holding(holding_dict: Dict, quote: Optional[Dict]) -> Dict:
    if not quote or not quote.get("price"):
        holding_dict.update({
            "current_price": None,
            "day_change_pct": None,
            "current_value": None,
            "unrealized_gain": None,
            "unrealized_gain_pct": None,
            "weight": None,
        })
        return holding_dict
    price = quote["price"]
    shares = holding_dict["shares"]
    avg_cost = holding_dict["avg_cost"]
    current_value = price * shares
    unrealized_gain = (price - avg_cost) * shares
    unrealized_gain_pct = ((price - avg_cost) / avg_cost * 100) if avg_cost else 0
    holding_dict.update({
        "current_price": price,
        "day_change_pct": quote.get("day_change_pct"),
        "current_value": round(current_value, 2),
        "unrealized_gain": round(unrealized_gain, 2),
        "unrealized_gain_pct": round(unrealized_gain_pct, 2),
        "company_name": quote.get("company_name"),
    })
    return holding_dict

def compute_portfolio_summary(enriched_holdings: List[Dict]) -> Dict:
    total_cost = sum(h["shares"] * h["avg_cost"] for h in enriched_holdings)
    total_value = sum(h.get("current_value") or (h["shares"] * h["avg_cost"]) for h in enriched_holdings)
    total_pnl = total_value - total_cost
    total_return_pct = ((total_value - total_cost) / total_cost * 100) if total_cost else 0

    # Assign weights
    for h in enriched_holdings:
        cv = h.get("current_value") or (h["shares"] * h["avg_cost"])
        h["weight"] = round((cv / total_value * 100) if total_value else 0, 2)

    return {
        "total_cost_basis": round(total_cost, 2),
        "total_market_value": round(total_value, 2),
        "total_unrealized_pnl": round(total_pnl, 2),
        "total_return_pct": round(total_return_pct, 2),
        "holdings_count": len(enriched_holdings),
    }
