"""Behavior routes for rule-based psychology analysis."""

from fastapi import APIRouter

from models.behavior_model import BehaviorAnalysisRequest
from services.behavior_analyzer import BehaviorAnalyzer

router = APIRouter()
behavior_analyzer = BehaviorAnalyzer()


@router.post("/analyze-behavior")
def analyze_behavior(payload: BehaviorAnalysisRequest):
    """Analyze recent trading decisions for psychology patterns."""
    return behavior_analyzer.analyze(payload)
