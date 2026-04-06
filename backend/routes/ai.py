"""AI routes for turning behavior signals into coaching feedback."""

from fastapi import APIRouter

from models.behavior_model import AIPipelineRequest, BehaviorAnalysisResult
from services.ai_service import AIService

router = APIRouter()
ai_service = AIService()


@router.post("/ai-feedback")
def run_ai_feedback_pipeline(payload: AIPipelineRequest):
    """Run the end-to-end AI feedback pipeline."""
    return ai_service.run_ai_pipeline(
        model_output=payload.model_output,
        trade_data=payload.trade_data,
        market_data=payload.market_data,
    )


@router.post("/ai-feedback/legacy")
def generate_feedback(payload: BehaviorAnalysisResult):
    """Generate natural-language coaching feedback from behavior labels."""
    return ai_service.generate_feedback(payload)
