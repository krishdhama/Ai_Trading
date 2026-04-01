"""AI routes for turning behavior signals into coaching feedback."""

from fastapi import APIRouter

from models.behavior_model import BehaviorAnalysisResult
from services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


@router.post("/ai-feedback")
def generate_feedback(payload: BehaviorAnalysisResult):
    """Generate natural-language coaching feedback from behavior labels."""
    return ai_service.generate_feedback(payload)
