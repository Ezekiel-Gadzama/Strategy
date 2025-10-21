from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum


class EventType(Enum):
    GOALS = "goals"
    CARDS = "cards"
    CORNERS = "corners"
    SHOTS = "shots"
    POSSESSION = "possession"
    FOULS = "fouls"
    OFFSIDES = "offsides"
    PASSES = "passes"
    HALF_STATS = "half_stats"
    TEAM_STATS = "team_stats"


@dataclass
class MatchEvent:
    event_type: EventType
    value: Any
    team: Optional[str] = None
    minute: Optional[int] = None
    is_home: Optional[bool] = None


@dataclass
class Match:
    id: int
    league: str
    season: int
    date: str
    home_team: str
    away_team: str
    score_home: int
    score_away: int
    events: List[MatchEvent]

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'league': self.league,
            'season': self.season,
            'date': self.date,
            'home_team': self.home_team,
            'away_team': self.away_team,
            'score_home': self.score_home,
            'score_away': self.score_away,
            'events': [{'type': e.event_type.value, 'value': e.value, 'team': e.team} for e in self.events]
        }


@dataclass
class EventPattern:
    events: List[MatchEvent]
    occurrence_count: int
    total_matches: int
    leagues: List[str]

    @property
    def percentage(self) -> float:
        return (self.occurrence_count / self.total_matches) * 100 if self.total_matches > 0 else 0