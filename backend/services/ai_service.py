"""LangChain-based Gemini service for generating trading psychology feedback."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from models.behavior_model import BehaviorAnalysisResult
from pydantic import BaseModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(Path(__file__).resolve().parents[1] / ".env")


behavior_history: list[str] = []


class FeedbackResponse(BaseModel):
    explanation: str
    mistake: str
    suggestion: str


class AIService:
    """Provide prompt building and LangChain-backed Gemini feedback."""

    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "")
        self.model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.client = (
            ChatGoogleGenerativeAI(
                model=self.model,
                google_api_key=self.api_key,
                temperature=0.2,
            )
            if self.api_key
            else None
        )

    def _build_prompt(self, payload: BehaviorAnalysisResult) -> str:
        return (
            "You are a trading psychology coach. "
            "Give concise, supportive feedback based on the detected behaviors.\n\n"
            f"Behaviors: {', '.join(payload.behaviors)}\n"
            f"Confidence: {payload.confidence}\n"
            f"Summary: {payload.summary}\n\n"
            "Return 3 short sections: observation, risk, next action."
        )

    def _safe_float(self, value: Any, default: float = 0.0) -> float:
        try:
            if value is None or value == "":
                return default
            return float(value)
        except (TypeError, ValueError):
            return default

    def _safe_text(self, value: Any, default: str = "unknown") -> str:
        if value is None:
            return default
        text = str(value).strip()
        return text if text else default

    def _normalize_model_output(self, model_output: dict[str, Any]) -> dict[str, Any]:
        """Accept either a single behavior label or analyzer-style behaviors list."""
        behavior = model_output.get("behavior")
        if behavior:
            return {
                "behavior": self._safe_text(behavior, "disciplined"),
                "confidence": self._safe_float(model_output.get("confidence")),
                "summary": self._safe_text(model_output.get("summary"), ""),
            }

        behaviors = model_output.get("behaviors") or []
        return {
            "behavior": self._safe_text(behaviors[0] if behaviors else "disciplined"),
            "confidence": self._safe_float(model_output.get("confidence")),
            "summary": self._safe_text(model_output.get("summary"), ""),
        }

    def build_insights(self, trade: dict[str, Any], market: dict[str, Any]) -> str:
        """Build a concise combined insight string from trade and market context."""
        insights: list[str] = []

        price_change_pct = self._safe_float(market.get("price_change_pct"))
        pnl_pct = self._safe_float(trade.get("pnl_pct"))
        holding_time = self._safe_float(trade.get("holding_time"))

        if price_change_pct > 0.05:
            insights.append("market already moved strongly")
        if pnl_pct < 0:
            insights.append("user currently in loss")
        if holding_time <= 1:
            insights.append("very quick reaction trade")

        return "; ".join(insights)

    def build_prompt(
        self,
        behavior: dict[str, Any] | str,
        trade: dict[str, Any],
        market: dict[str, Any],
        insights: str,
    ) -> str:
        """Build a concise, context-aware coaching prompt for the LLM."""
        if isinstance(behavior, dict):
            normalized_behavior = self._normalize_model_output(behavior)
            behavior_label = normalized_behavior["behavior"]
            confidence = self._safe_float(normalized_behavior.get("confidence"))
        else:
            behavior_label = self._safe_text(behavior)
            confidence = 0.0

        action = self._safe_text(trade.get("action"))
        price = self._safe_text(trade.get("price"))
        price_change_pct = self._safe_float(market.get("price_change_pct"))
        trend = self._safe_text(market.get("trend"))

        return (
            "You are an expert trading psychology coach and behavioral analyst.\n\n"
            "Context:\n"
            f"- User action: {action}\n"
            f"- Executed price: {price}\n"
            f"- Market price change %: {price_change_pct}\n"
            f"- Trend: {trend}\n"
            f"- Behavior label: {behavior_label}\n"
            f"- Confidence: {confidence:.2f}\n"
            f"- Insights: {insights or 'none'}\n\n"
            "Task:\n"
            "Analyze the likely psychology behind the decision using the real context above. "
            "Keep it concise and specific.\n\n"
            "Return valid JSON only with these keys:\n"
            '- "explanation"\n'
            '- "mistake"\n'
            '- "suggestion"'
        )

    def _generate_insights(
        self,
        model_output: dict[str, Any],
        trade_data: dict[str, Any],
        market_data: dict[str, Any],
    ) -> str:
        normalized_output = self._normalize_model_output(model_output)
        action = self._safe_text(trade_data.get("action"), "unknown")
        pnl_pct = self._safe_float(trade_data.get("pnl_pct"))
        holding_time = self._safe_text(trade_data.get("holding_time"), "unknown")
        price_change_pct = self._safe_float(market_data.get("price_change_pct"))
        trend = self._safe_text(market_data.get("trend"), "unknown")
        volatility = self._safe_text(market_data.get("volatility"), "unknown")
        behavior = normalized_output["behavior"]
        confidence = self._safe_float(normalized_output.get("confidence"))
        summary = self._safe_text(normalized_output.get("summary"), "")

        insights: list[str] = [
            f"The user chose to {action.lower()} while the market trend was {trend}.",
            f"Position outcome was {pnl_pct:.2f}% over a holding time of {holding_time}.",
            f"Market moved {price_change_pct:.2f}% with {volatility} volatility.",
            f"Behavior model flagged {behavior} with {confidence:.2f} confidence.",
        ]
        if summary:
            insights.append(f"Behavior summary: {summary}.")
        rules_based_insights = self.build_insights(trade_data, market_data)
        if rules_based_insights:
            insights.append(f"Key context: {rules_based_insights}.")
        if behavior_history.count(behavior) >= 2:
            insights.append("You are repeating this mistake.")

        if action.upper() == "SELL" and price_change_pct < 0:
            insights.append("The exit happened into weakness, which can reflect pressure to avoid further pain.")
        elif action.upper() == "BUY" and price_change_pct > 0:
            insights.append("The entry followed positive price movement, which can reflect urgency or chasing.")

        if pnl_pct < 0:
            insights.append("A losing position can amplify emotional decision-making and shorten patience.")

        return " ".join(insights)

    def _build_pipeline_prompt(
        self,
        model_output: dict[str, Any],
        trade_data: dict[str, Any],
        market_data: dict[str, Any],
        insights: str,
    ) -> str:
        return self.build_prompt(
            behavior=model_output,
            trade=trade_data,
            market=market_data,
            insights=insights,
        )

    def _fallback_feedback(
        self,
        model_output: dict[str, Any],
        trade_data: dict[str, Any],
        market_data: dict[str, Any],
        insights: str,
    ) -> dict[str, str]:
        action = self._safe_text(trade_data.get("action"))
        pnl_pct = self._safe_float(trade_data.get("pnl_pct"))
        price_change_pct = self._safe_float(market_data.get("price_change_pct"))
        behavior = self._safe_text(model_output.get("behavior"), "reactive decision-making")

        explanation = (
            f"You likely {action.lower()}ed because the market moved {price_change_pct:.2f}% "
            f"and the trade sat at {pnl_pct:.2f}% PnL, which fits a {behavior} response."
        )
        mistake = (
            f"The main mistake was letting the {behavior} signal outweigh a planned response "
            f"to a {price_change_pct:.2f}% move."
        )
        suggestion = (
            "A disciplined trader would pause, define the invalidation level first, "
            "and act only if that pre-set condition was hit."
        )
        return {
            "explanation": explanation,
            "mistake": mistake,
            "suggestion": suggestion,
        }

    def call_llm(self, prompt: str) -> dict[str, str]:
        """Call Gemini through LangChain and return structured JSON feedback."""
        if not self.client:
            raise RuntimeError("GEMINI_API_KEY is not configured.")

        prompt_template = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert trading psychology coach and behavioral analyst. "
                    "Return only the requested structured output.",
                ),
                ("human", "{prompt}"),
            ]
        )
        structured_llm = self.client.with_structured_output(
            FeedbackResponse,
        )
        chain = prompt_template | structured_llm
        parsed = chain.invoke({"prompt": prompt})
        if not parsed:
            raise ValueError("Gemini returned an empty structured response.")

        if isinstance(parsed, FeedbackResponse):
            parsed_data = parsed.model_dump()
        elif isinstance(parsed, dict):
            parsed_data = parsed
        else:
            raise ValueError("Gemini returned an unexpected structured response type.")

        return {
            "explanation": self._safe_text(parsed_data.get("explanation"), ""),
            "mistake": self._safe_text(parsed_data.get("mistake"), ""),
            "suggestion": self._safe_text(parsed_data.get("suggestion"), ""),
        }

    def run_ai_pipeline(
        self,
        model_output: dict[str, Any],
        trade_data: dict[str, Any],
        market_data: dict[str, Any],
    ) -> dict[str, Any]:
        normalized_output = self._normalize_model_output(model_output)
        behavior = normalized_output["behavior"]
        confidence = self._safe_float(normalized_output.get("confidence"))
        score = 100
        if "FOMO" in behavior.upper() or "PANIC" in behavior.upper():
            score -= 20
        behavior_history.append(behavior)

        insights = self._generate_insights(normalized_output, trade_data, market_data)
        prompt = self.build_prompt(normalized_output, trade_data, market_data, insights)
        source = "gemini"
        try:
            llm_output = self.call_llm(prompt)
        except (RuntimeError, ValueError, json.JSONDecodeError, KeyError, TypeError):
            source = "fallback"
            llm_output = self._fallback_feedback(
                model_output=normalized_output,
                trade_data=trade_data,
                market_data=market_data,
                insights=insights,
            )
        return {
            "behavior": behavior,
            "confidence": confidence,
            "score": score,
            "source": source,
            "model_output": normalized_output,
            "trade_data": trade_data,
            "market_data": market_data,
            "feedback": llm_output,
        }

    def generate_feedback(self, payload: BehaviorAnalysisResult) -> dict:
        prompt = self._build_prompt(payload)

        feedback = (
            "Observation: Your recent trades show emotional pressure points. "
            "Risk: Reacting to price spikes or drops can break discipline. "
            "Next action: Pause before the next trade and define entry, exit, and risk."
        )
        source = "fallback"
        if self.client:
            try:
                feedback_json = self.call_llm(prompt)
                feedback = (
                    f"Explanation: {feedback_json['explanation']} "
                    f"Mistake: {feedback_json['mistake']} "
                    f"Suggestion: {feedback_json['suggestion']}"
                )
                source = "gemini"
            except (RuntimeError, ValueError, json.JSONDecodeError, KeyError, TypeError):
                source = "fallback"
        return {
            "feedback": feedback,
            "source": source,
            "prompt_used": prompt,
        }


def run_ai_pipeline(
    model_output: dict[str, Any],
    trade_data: dict[str, Any],
    market_data: dict[str, Any],
) -> dict[str, Any]:
    """Module-level entry point for orchestrating AI trading feedback."""
    return AIService().run_ai_pipeline(model_output, trade_data, market_data)


def build_insights(trade: dict[str, Any], market: dict[str, Any]) -> str:
    """Module-level helper for assembling rules-based insight strings."""
    return AIService().build_insights(trade, market)


def build_prompt(
    behavior: dict[str, Any] | str,
    trade: dict[str, Any],
    market: dict[str, Any],
    insights: str,
) -> str:
    """Module-level helper for assembling the LLM prompt."""
    return AIService().build_prompt(behavior, trade, market, insights)


def call_llm(prompt: str) -> dict[str, str]:
    """Module-level helper for Gemini structured output."""
    return AIService().call_llm(prompt)
