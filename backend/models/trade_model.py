"""Trade request and record models."""

from typing import Literal

from pydantic import BaseModel, Field


class TradeRequest(BaseModel):
    symbol: str = Field(..., examples=["AAPL"])
    side: Literal["BUY", "SELL"]
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)


class TradeRecord(BaseModel):
    symbol: str
    side: Literal["BUY", "SELL"]
    quantity: int
    price: float
    timestamp: str
