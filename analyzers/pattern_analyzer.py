from typing import List, Dict, Any, Set, Tuple
from itertools import combinations
from collections import defaultdict, Counter
import logging
from data.models import Match, EventPattern
from patterns.event_patterns import EventPatterns, EventCondition
from config.settings import AnalysisConfig


class PatternAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.all_patterns = EventPatterns.get_all_patterns()

    def analyze_matches(self, matches: List[Match]) -> Dict[str, Any]:
        """Analyze matches to find event patterns"""
        self.logger.info(f"Analyzing {len(matches)} matches for event patterns")

        # Find patterns that occur in each match
        match_patterns = self._find_match_patterns(matches)

        # Analyze combinations
        never_occurred = self._find_never_occurred_combinations(match_patterns, matches)
        least_occurred = self._find_least_occurred_combinations(match_patterns, matches)
        most_occurred = self._find_most_occurred_combinations(match_patterns, matches)

        return {
            'never_occurred': never_occurred,
            'least_occurred': least_occurred,
            'most_occurred': most_occurred,
            'total_matches': len(matches),
            'total_patterns_analyzed': len(self.all_patterns)
        }

    def _find_match_patterns(self, matches: List[Match]) -> Dict[int, Set[str]]:
        """Find which patterns occur in each match"""
        match_patterns = {}

        for match in matches:
            occurring_patterns = set()
            for pattern in self.all_patterns:
                if pattern.condition(match):
                    occurring_patterns.add(pattern.name)
            match_patterns[match.id] = occurring_patterns

        return match_patterns

    def _find_never_occurred_combinations(self, match_patterns: Dict[int, Set[str]],
                                          matches: List[Match]) -> List[Dict[str, Any]]:
        """Find combinations of events that never occurred together"""
        all_pattern_names = [p.name for p in self.all_patterns]
        combination_occurrence = defaultdict(int)

        # Check all combinations of specified size range
        for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
            for combo in combinations(all_pattern_names, size):
                combo_set = set(combo)
                occurred_count = sum(1 for patterns in match_patterns.values()
                                     if combo_set.issubset(patterns))
                combination_occurrence[combo] = occurred_count

        # Filter never occurred combinations
        never_occurred = []
        for combo, count in combination_occurrence.items():
            if count == 0:
                pattern_details = [EventPatterns.get_pattern_by_name(name) for name in combo]
                never_occurred.append({
                    'events': [{'name': p.name, 'description': p.description} for p in pattern_details],
                    'combination_size': len(combo),
                    'occurrence_count': 0,
                    'percentage': 0.0
                })

        return never_occurred[:10]  # Return top 10

    def _find_least_occurred_combinations(self, match_patterns: Dict[int, Set[str]],
                                          matches: List[Match]) -> List[Dict[str, Any]]:
        """Find combinations of events that occurred least frequently"""
        all_pattern_names = [p.name for p in self.all_patterns]
        combination_occurrence = Counter()

        # Count occurrences of each combination
        for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
            for match_id, patterns in match_patterns.items():
                pattern_list = list(patterns)
                if len(pattern_list) >= size:
                    for combo in combinations(pattern_list, size):
                        combination_occurrence[combo] += 1

        # Filter by minimum threshold and get least occurred
        total_matches = len(matches)
        least_occurred = []

        for combo, count in combination_occurrence.most_common():
            percentage = (count / total_matches) * 100
            if percentage <= self.config.MIN_OCCURRENCE_THRESHOLD * 100:
                pattern_details = [EventPatterns.get_pattern_by_name(name) for name in combo]
                least_occurred.append({
                    'events': [{'name': p.name, 'description': p.description} for p in pattern_details],
                    'combination_size': len(combo),
                    'occurrence_count': count,
                    'percentage': percentage,
                    'leagues': self._get_leagues_for_combination(combo, matches, match_patterns)
                })

        return least_occurred[:10]

    def _find_most_occurred_combinations(self, match_patterns: Dict[int, Set[str]],
                                         matches: List[Match]) -> List[Dict[str, Any]]:
        """Find combinations of events that occurred most frequently"""
        all_pattern_names = [p.name for p in self.all_patterns]
        combination_occurrence = Counter()

        # Count occurrences of each combination
        for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
            for match_id, patterns in match_patterns.items():
                pattern_list = list(patterns)
                if len(pattern_list) >= size:
                    for combo in combinations(pattern_list, size):
                        combination_occurrence[combo] += 1

        # Get most occurred combinations
        most_occurred = []
        total_matches = len(matches)

        for combo, count in combination_occurrence.most_common(10):
            percentage = (count / total_matches) * 100
            pattern_details = [EventPatterns.get_pattern_by_name(name) for name in combo]
            most_occurred.append({
                'events': [{'name': p.name, 'description': p.description} for p in pattern_details],
                'combination_size': len(combo),
                'occurrence_count': count,
                'percentage': percentage,
                'leagues': self._get_leagues_for_combination(combo, matches, match_patterns)
            })

        return most_occurred

    def _get_leagues_for_combination(self, combo: Tuple[str], matches: List[Match],
                                     match_patterns: Dict[int, Set[str]]) -> List[str]:
        """Get leagues where a combination occurred"""
        combo_set = set(combo)
        leagues = set()

        for match_id, patterns in match_patterns.items():
            if combo_set.issubset(patterns):
                match = next((m for m in matches if m.id == match_id), None)
                if match:
                    leagues.add(match.league)

        return list(leagues)