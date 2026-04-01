"""OpenAI integration service for generating coaching-style feedback."""

from __future__ import annotations

import os

from openai import OpenAI

from models.behavior_model import BehaviorAnalysisResult


class AIService:
    """Wrap OpenAI calls and provide a safe fallback when no API key is set."""

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def _build_prompt(self, payload: BehaviorAnalysisResult) -> str:
        return (
            "You are a trading psychology coach. "
            "Give concise, supportive feedback based on the detected behaviors.\n\n"
            f"Behaviors: {', '.join(payload.behaviors)}\n"
            f"Confidence: {payload.confidence}\n"
            f"Summary: {payload.summary}\n\n"
            "Return 3 short sections: observation, risk, next action."
        )

    def generate_feedback(self, payload: BehaviorAnalysisResult) -> dict:
        prompt = self._build_prompt(payload)

        if not self.client:
            return {
                "feedback": (
                    "Observation: Your recent trades show emotional pressure points. "
                    "Risk: Reacting to price spikes or drops can break discipline. "
                    "Next action: Pause before the next trade and define entry, exit, and risk."
                ),
                "source": "fallback",
                "prompt_used": prompt,
            }

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return {
            "feedback": response.output_text,
            "source": "openai",
            "prompt_used": prompt,
        }
