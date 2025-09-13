from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any
import time

class Action(str, Enum):
    WATCHLISTED = "WATCHLISTED"
    RATED = "RATED"

@dataclass
class ActivityEvent:
    userId: str
    movieId: str
    action: Action
    timestamp: int           # unix ms

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        # Remove None values to keep the payload minimal
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def now(user_id: str, movie_id: str, action: Action) -> "ActivityEvent":
        ts_ms = int(time.time() * 1000)
        return ActivityEvent(userId=user_id, movieId=movie_id, action=action, timestamp=ts_ms)
