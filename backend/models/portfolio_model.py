"""Portfolio state model used by the trade engine and API."""

from pydantic import BaseModel


class PortfolioState(BaseModel):
    cash: float
    holdings: dict[str, int]
    total_value: float
