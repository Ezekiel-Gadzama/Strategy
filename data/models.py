from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class EventType(Enum):
    SHOT_ON_TARGET = "shot_on_target"
    GOALS = "goals"
    CARDS = "cards"
    CORNER = "corners"
    SHOTS = "shots"
    POSSESSION = "possession"
    FOULS = "fouls"
    OFFSIDES = "offsides"
    PASSES = "passes"
    HALF_STATS = "half_stats"
    TEAM_STATS = "team_stats"
    YELLOW_CARD = "yellow_card"
    RED_CARD = "red_card"
    SECOND_YELLOW = "second_yellow"
    PENALTY_AWARDED = "penalty_awarded"
    THROW_IN = "throw_in"
    FREE_KICK = "free_kick"
    GOAL_KICK = "goal_kick"


@dataclass
class MatchEvent:
    event_type: EventType
    value: Any
    team: Optional[str] = None
    minute: Optional[int] = None
    is_home: Optional[bool] = None
    description: Optional[str] = None

    def __post_init__(self):
        """Handle both 'type' and 'event_type' parameter names for backward compatibility"""
        pass

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'MatchEvent':
        """Create MatchEvent from dictionary (handles both old and new parameter names)"""
        # Handle both 'type' and 'event_type' for backward compatibility
        if 'type' in data and 'event_type' not in data:
            data = data.copy()
            data['event_type'] = data.pop('type')

        # Convert string event_type back to EventType enum if needed
        if isinstance(data.get('event_type'), str):
            try:
                data['event_type'] = EventType(data['event_type'])
            except ValueError:
                # Handle unknown event types gracefully
                data['event_type'] = EventType.TEAM_STATS  # default

        return cls(**data)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'event_type': self.event_type.value,  # Save as string for JSON
            'value': self.value,
            'team': self.team,
            'minute': self.minute,
            'is_home': self.is_home,
            'description': self.description
        }


@dataclass
class TeamStats:
    team_id: int
    team_name: str
    shots_on_goal: int = 0
    shots_off_goal: int = 0
    shots_insidebox: int = 0
    shots_outsidebox: int = 0
    total_shots: int = 0
    blocked_shots: int = 0
    fouls: int = 0
    corner_kicks: int = 0
    offsides: int = 0
    ball_possession: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    goalkeeper_saves: int = 0
    total_passes: int = 0
    passes_accurate: int = 0
    passes_percentage: float = 0.0


@dataclass
class HalfStats:
    home_goals: int = 0
    away_goals: int = 0
    home_cards: int = 0
    away_cards: int = 0
    home_corners: int = 0
    away_corners: int = 0


@dataclass
class Match:
    id: int
    league: str
    league_id: int
    season: int
    date: str
    home_team: str
    home_team_id: int
    away_team: str
    away_team_id: int
    score_home: int
    score_away: int
    status: str
    venue: Optional[str] = None

    # Detailed statistics
    home_stats: TeamStats = None
    away_stats: TeamStats = None
    first_half: HalfStats = field(default_factory=HalfStats)
    second_half: HalfStats = field(default_factory=HalfStats)

    # Events
    events: List[MatchEvent] = field(default_factory=list)

    # Additional match details
    referee: Optional[str] = None
    venue_id: Optional[int] = None
    venue_city: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'league': self.league,
            'league_id': self.league_id,
            'season': self.season,
            'date': self.date,
            'home_team': self.home_team,
            'home_team_id': self.home_team_id,
            'away_team': self.away_team,
            'away_team_id': self.away_team_id,
            'score_home': self.score_home,
            'score_away': self.score_away,
            'status': self.status,
            'events': [e.to_dict() for e in self.events],
            'home_stats': self.home_stats.__dict__ if self.home_stats else {},
            'away_stats': self.away_stats.__dict__ if self.away_stats else {},
            'first_half': self.first_half.__dict__,
            'second_half': self.second_half.__dict__
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
