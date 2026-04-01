"""Models for behavior analysis inputs and outputs."""

from pydantic import BaseModel

from models.trade_model import TradeRecord


class BehaviorAnalysisRequest(BaseModel):
    recent_trades: list[TradeRecord] = []
    market_change_pct: float = 0.0
    unrealized_pnl_pct: float = 0.0
    holding_duration_days: int = 0


class BehaviorAnalysisResult(BaseModel):
    behaviors: list[str]
    confidence: float
    summary: str
