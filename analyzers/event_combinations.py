from typing import List, Set, Tuple, Dict, Any
from itertools import combinations
import logging

class EventCombinationGenerator:
    def __init__(self, min_events: int = 3, max_events: int = 5):
        self.min_events = min_events
        self.max_events = max_events
        self.logger = logging.getLogger(__name__)

    def generate_combinations(self, all_event_types: List[str]) -> List[Tuple[str]]:
        """Generate all possible combinations of event types"""
        all_combinations = []

        for size in range(self.min_events, self.max_events + 1):
            for combo in combinations(all_event_types, size):
                all_combinations.append(combo)

        self.logger.info(f"Generated {len(all_combinations)} combinations of size {self.min_events}-{self.max_events}")
        return all_combinations

    def filter_meaningful_combinations(self, combinations: List[Tuple[str]],
                                       event_categories: Dict[str, str]) -> List[Tuple[str]]:
        """Filter combinations to include only meaningful ones (events from different categories)"""
        meaningful_combos = []

        for combo in combinations:
            categories = set()
            for event in combo:
                category = event_categories.get(event, 'unknown')
                categories.add(category)

            # Prefer combinations with events from different categories
            if len(categories) >= self.min_events - 1:
                meaningful_combos.append(combo)

        return meaningful_combos
