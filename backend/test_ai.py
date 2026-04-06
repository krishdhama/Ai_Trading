"""Simple local test script for the AI feedback pipeline."""

from __future__ import annotations

from dotenv import load_dotenv

from services.ai_service import run_ai_pipeline

load_dotenv()


def prompt_text(label: str, default: str) -> str:
    value = input(f"{label} [{default}]: ").strip()
    return value or default


def prompt_float(label: str, default: float) -> float:
    value = input(f"{label} [{default}]: ").strip()
    if not value:
        return default
    return float(value)


def main() -> None:
    print("Enter static values for the AI pipeline test.")
    print("Press Enter to use the default value shown in brackets.")
    print()

    model_output = {
        "behavior": prompt_text("Behavior label", "FOMO_BUY"),
        "confidence": prompt_float("Confidence", 0.82),
    }

    trade_data = {
        "action": prompt_text("Trade action", "BUY"),
        "price": prompt_float("Executed price", 245.50),
        "pnl_pct": prompt_float("PnL %", -2.4),
        "holding_time": prompt_float("Holding time", 1),
    }

    market_data = {
        "current_price": prompt_float("Current price", 248.10),
        "prev_price": prompt_float("Previous price", 233.40),
        "price_change_pct": prompt_float("Price change %", 0.063),
        "trend": prompt_text("Trend", "uptrend"),
        "volatility": prompt_text("Volatility", "high"),
    }

    result = run_ai_pipeline(model_output, trade_data, market_data)
    behavior = result.get("behavior", "UNKNOWN")
    confidence = float(result.get("confidence", 0.0)) * 100
    score = result.get("score", 0)
    feedback = result["feedback"]

    print(f"Behavior: {behavior} ({confidence:.0f}%)")
    print(f"Score: {score}")
    print()
    print(f"Explanation: {feedback.get('explanation', '')}")
    print(f"Mistake: {feedback.get('mistake', '')}")
    print(f"Suggestion: {feedback.get('suggestion', '')}")


if __name__ == "__main__":
    main()
