from dataclasses import dataclass

@dataclass(frozen=True)
class User:
    """class User that contains information about user (only their name by now)"""
    name: str
