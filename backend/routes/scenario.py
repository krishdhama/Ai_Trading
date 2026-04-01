"""Scenario routes for simulation start and day progression."""

from fastapi import APIRouter

from services.scenario_engine import ScenarioEngine

router = APIRouter()
scenario_engine = ScenarioEngine()


@router.get("/init")
def init_scenario():
    """Return the first market snapshot and reset simulation state."""
    return scenario_engine.initialize()


@router.post("/next-day")
def next_day():
    """Advance the scenario by one day and return updated market data."""
    return scenario_engine.next_day()
