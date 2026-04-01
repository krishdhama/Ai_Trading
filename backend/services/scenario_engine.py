"""Scenario engine that loads price data and steps through it day by day."""

from __future__ import annotations

import csv
import os
from pathlib import Path


class ScenarioEngine:
    """Simple CSV-backed day progression engine for hackathon simulations."""

    def __init__(self) -> None:
        self.current_index = 0
        self.rows = self._load_price_data()

    def _load_price_data(self) -> list[dict]:
        env_path = os.getenv("PRICE_DATA_PATH", "backend/data/sample_prices.csv")
        csv_path = Path(env_path)
        if not csv_path.exists():
            return [{"date": "2025-01-01", "price": 100.0}]

        with csv_path.open("r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [
                {
                    "date": row["date"],
                    "price": float(row["price"]),
                }
                for row in reader
            ] or [{"date": "2025-01-01", "price": 100.0}]

    def initialize(self) -> dict:
        self.current_index = 0
        return {
            "message": "Scenario initialized",
            "current_day": self.current_index,
            "market": self.rows[self.current_index],
        }

    def next_day(self) -> dict:
        if self.current_index < len(self.rows) - 1:
            self.current_index += 1

        return {
            "message": "Advanced to next day",
            "current_day": self.current_index,
            "market": self.rows[self.current_index],
            "is_last_day": self.current_index == len(self.rows) - 1,
        }
