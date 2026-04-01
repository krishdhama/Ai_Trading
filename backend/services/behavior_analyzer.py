"""Rule-based behavior analyzer for trading psychology patterns."""

from __future__ import annotations

from models.behavior_model import BehaviorAnalysisRequest, BehaviorAnalysisResult


class BehaviorAnalyzer:
    """Detect hackathon-friendly behavior signals from recent trades."""

    def analyze(self, payload: BehaviorAnalysisRequest) -> dict:
        labels: list[str] = []
        notes: list[str] = []

        trade_count = len(payload.recent_trades)
        latest_trade = payload.recent_trades[-1] if payload.recent_trades else None

        if latest_trade and latest_trade.side == "SELL" and payload.market_change_pct <= -5:
            labels.append("panic_sell")
            notes.append("User sold into a sharp drop, which may reflect fear-based decision making.")

        if latest_trade and latest_trade.side == "BUY" and payload.market_change_pct >= 5:
            labels.append("fomo_buy")
            notes.append("User bought after a strong move up, suggesting momentum chasing.")

        if trade_count >= 5:
            labels.append("overtrading")
            notes.append("User placed many trades in a short window, which can signal impulsive execution.")

        if payload.unrealized_pnl_pct <= -10 and payload.holding_duration_days >= 5:
            labels.append("loss_holding")
            notes.append("User is holding a losing position for a prolonged period without evidence of a plan.")

        result = BehaviorAnalysisResult(
            behaviors=labels or ["disciplined"],
            confidence=0.72 if labels else 0.9,
            summary=" | ".join(notes) if notes else "No major behavior flags detected.",
        )
        return result.model_dump()
