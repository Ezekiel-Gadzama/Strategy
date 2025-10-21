from typing import List, Dict, Any, Callable
from dataclasses import dataclass
from data.models import Match, MatchEvent, EventType


@dataclass
class EventCondition:
    name: str
    description: str
    condition: Callable[[Match], bool]
    event_type: EventType


class EventPatterns:
    """Define various event patterns to analyze"""

    @staticmethod
    def get_all_patterns() -> List[EventCondition]:
        return [
            # Goal-related patterns
            EventCondition(
                name="high_scoring",
                description="Total goals over 4.5",
                condition=lambda m: (m.score_home + m.score_away) > 4.5,
                event_type=EventType.GOALS
            ),
            EventCondition(
                name="low_scoring",
                description="Total goals under 1.5",
                condition=lambda m: (m.score_home + m.score_away) < 1.5,
                event_type=EventType.GOALS
            ),
            EventCondition(
                name="both_teams_score",
                description="Both teams scored",
                condition=lambda m: m.score_home > 0 and m.score_away > 0,
                event_type=EventType.GOALS
            ),
            EventCondition(
                name="clean_sheet_home",
                description="Home team clean sheet",
                condition=lambda m: m.score_away == 0,
                event_type=EventType.GOALS
            ),
            EventCondition(
                name="clean_sheet_away",
                description="Away team clean sheet",
                condition=lambda m: m.score_home == 0,
                event_type=EventType.GOALS
            ),

            # Card-related patterns (placeholder - would be populated with real data)
            EventCondition(
                name="many_cards",
                description="Total cards over 5.5",
                condition=lambda m: True,  # Would check actual card data
                event_type=EventType.CARDS
            ),
            EventCondition(
                name="few_cards",
                description="Total cards under 2.5",
                condition=lambda m: True,  # Would check actual card data
                event_type=EventType.CARDS
            ),

            # Corner-related patterns
            EventCondition(
                name="many_corners",
                description="Total corners over 10.5",
                condition=lambda m: True,  # Would check actual corner data
                event_type=EventType.CORNERS
            ),

            # Shot-related patterns
            EventCondition(
                name="many_shots",
                description="Total shots over 20.5",
                condition=lambda m: True,  # Would check actual shot data
                event_type=EventType.SHOTS
            ),

            # Half-time patterns
            EventCondition(
                name="goals_first_half",
                description="Goals scored in first half",
                condition=lambda m: True,  # Would check half-time data
                event_type=EventType.HALF_STATS
            ),

            # Team performance patterns
            EventCondition(
                name="high_possession",
                description="Home team possession over 60%",
                condition=lambda m: True,  # Would check possession data
                event_type=EventType.POSSESSION
            ),

            # Add more patterns as needed based on available data
        ]

    @staticmethod
    def get_pattern_by_name(name: str) -> EventCondition:
        patterns = {p.name: p for p in EventPatterns.get_all_patterns()}
        return patterns.get(name)
