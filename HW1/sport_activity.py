from user import User
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class SportActivty:
    """class SportActivty that contains information about activty: user who created it, activity name, planned time and location"""
    author: User
    name: str
    planned_at: datetime
    place: str
