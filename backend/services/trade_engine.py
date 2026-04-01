"""Trade engine for buy/sell execution and mock portfolio tracking."""

from __future__ import annotations

from datetime import datetime

from models.portfolio_model import PortfolioState
from models.trade_model import TradeRequest


class TradeEngine:
    """In-memory trade engine suitable for a hackathon starter build."""

    def __init__(self) -> None:
        self.portfolio = PortfolioState(cash=10000.0, holdings={}, total_value=10000.0)
        self.trade_history: list[dict] = []

    def execute_trade(self, payload: TradeRequest) -> dict:
        symbol = payload.symbol.upper()
        quantity = payload.quantity
        price = payload.price
        cost = quantity * price
        current_position = self.portfolio.holdings.get(symbol, 0)

        if payload.side == "BUY":
            if self.portfolio.cash < cost:
                raise ValueError("Insufficient cash for this trade.")
            self.portfolio.cash -= cost
            self.portfolio.holdings[symbol] = current_position + quantity

        if payload.side == "SELL":
            if current_position < quantity:
                raise ValueError("Not enough shares to sell.")
            self.portfolio.cash += cost
            updated_position = current_position - quantity
            if updated_position == 0:
                self.portfolio.holdings.pop(symbol, None)
            else:
                self.portfolio.holdings[symbol] = updated_position

        trade_record = {
            "symbol": symbol,
            "side": payload.side,
            "quantity": quantity,
            "price": price,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self.trade_history.append(trade_record)
        self._recalculate_total_value(last_price_map={symbol: price})

        return {
            "message": "Trade executed successfully",
            "portfolio": self.portfolio.model_dump(),
            "trade": trade_record,
        }

    def _recalculate_total_value(self, last_price_map: dict[str, float]) -> None:
        holdings_value = sum(
            quantity * last_price_map.get(symbol, 0.0)
            for symbol, quantity in self.portfolio.holdings.items()
        )
        self.portfolio.total_value = round(self.portfolio.cash + holdings_value, 2)

    def get_portfolio(self) -> dict:
        return self.portfolio.model_dump()

    def get_trade_history(self) -> list[dict]:
        return self.trade_history
