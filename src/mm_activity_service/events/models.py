from dataclasses import dataclass, asdict
from typing import Optional
from enum import Enum
import time

class Action(str, Enum):
    WATCHLISTED = "WATCHLISTED"
    RATED = "RATED"

@dataclass
class ActivityEvent:
    userId: str
    movieId: str
    action: Action
    timestamp: int

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def now(user_id: str, movie_id: str, action: Action) -> "ActivityEvent":
        ts_ms = int(time.time() * 1000)
        return ActivityEvent(userId=user_id, movieId=movie_id, action=action, timestamp=ts_ms)

@dataclass
class RatedEvent(ActivityEvent):
    rating: int

    def __init__(self, userId: str, movieId: str, rating: int, timestamp: Optional[int] = None):
        super().__init__(
            userId=userId,
            movieId=movieId,
            action=Action.RATED,
            timestamp=timestamp or int(time.time() * 1000)
        )
        self.rating = rating

@dataclass
class WatchlistedEvent(ActivityEvent):
    def __init__(self, userId: str, movieId: str, timestamp: Optional[int] = None):
        super().__init__(
            userId=userId,
            movieId=movieId,
            action=Action.WATCHLISTED,
            timestamp=timestamp or int(time.time() * 1000)
        )
