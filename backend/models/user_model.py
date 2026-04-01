"""User model for future authentication and profile expansion."""

from pydantic import BaseModel


class UserModel(BaseModel):
    user_id: str
    name: str
    xp: int = 0
    risk_profile: str = "balanced"
