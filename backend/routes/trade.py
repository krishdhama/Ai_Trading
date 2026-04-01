"""Trade routes for buy/sell execution and portfolio history access."""

from fastapi import APIRouter, HTTPException

from models.trade_model import TradeRequest
from services.trade_engine import TradeEngine

router = APIRouter()
trade_engine = TradeEngine()


@router.post("/trade")
def execute_trade(payload: TradeRequest):
    """Execute a buy or sell trade against the current mock portfolio."""
    try:
        result = trade_engine.execute_trade(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return result


@router.get("/portfolio")
def get_portfolio():
    """Return the current portfolio snapshot."""
    return trade_engine.get_portfolio()


@router.get("/trade-history")
def get_trade_history():
    """Return recent executed trades."""
    return {"trades": trade_engine.get_trade_history()}
