"""Models for behavior analysis inputs and outputs."""

from typing import Any

from pydantic import BaseModel, Field

from models.trade_model import TradeRecord


class BehaviorAnalysisRequest(BaseModel):
    recent_trades: list[TradeRecord] = Field(default_factory=list)
    market_change_pct: float = 0.0
    unrealized_pnl_pct: float = 0.0
    holding_duration_days: int = 0


class BehaviorAnalysisResult(BaseModel):
    behaviors: list[str]
    confidence: float
    summary: str


class AIPipelineRequest(BaseModel):
    model_output: dict[str, Any]
    trade_data: dict[str, Any]
    market_data: dict[str, Any]
