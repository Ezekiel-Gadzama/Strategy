from typing import List, Dict, Any, Set, Tuple
from itertools import combinations
from collections import Counter
import logging
from data.models import Match
from patterns.event_patterns import EventPatterns, EventCondition
from config.settings import AnalysisConfig


class PatternAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.all_patterns = EventPatterns.get_all_patterns()

    def analyze_matches(self, matches: List[Match]) -> Dict[str, Any]:
        """Analyze matches league by league."""
        leagues = set(m.league for m in matches)
        league_results = {}

        for league in leagues:
            league_matches = [m for m in matches if m.league == league]
            self.logger.info(f"Analyzing {len(league_matches)} matches in {league}")

            match_patterns = self._find_match_patterns(league_matches)

            league_results[league] = {
                'never_occurred': self._find_never_occurred_combinations(match_patterns, league_matches),
                'least_occurred': self._find_least_occurred_combinations(match_patterns, league_matches),
                'most_occurred': self._find_most_occurred_combinations(match_patterns, league_matches),
                'total_matches': len(league_matches),
                'total_patterns_analyzed': len(self.all_patterns)
            }

        return league_results

    def _find_match_patterns(self, matches: List[Match]) -> Dict[int, Set[str]]:
        match_patterns = {}

        for match in matches:
            occurring_patterns = set()
            for pattern in self.all_patterns:
                try:
                    if pattern.condition(match):
                        occurring_patterns.add(pattern.name)
                except Exception:
                    continue
            match_patterns[match.id] = occurring_patterns

        return match_patterns

    def _valid_combination(self, combo: Tuple[str]) -> bool:
        """Ensure no two events share the same market."""
        market_seen = set()
        for name in combo:
            pattern = EventPatterns.get_pattern_by_name(name)
            if pattern is None:
                return False
            if pattern.market in market_seen:
                return False
            market_seen.add(pattern.market)
        return True

    def _find_never_occurred_combinations(self, match_patterns: Dict[int, Set[str]], matches: List[Match]) -> List[Dict[str, Any]]:
        all_pattern_names = [p.name for p in self.all_patterns]
        never_occurred = []

        for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
            for combo in combinations(all_pattern_names, size):
                if not self._valid_combination(combo):
                    continue
                occurred_count = sum(1 for patterns in match_patterns.values() if set(combo).issubset(patterns))
                if occurred_count == 0:
                    pattern_details = [EventPatterns.get_pattern_by_name(name) for name in combo]
                    never_occurred.append({
                        'events': [{'name': p.name, 'description': p.description} for p in pattern_details],
                        'combination_size': len(combo),
                        'occurrence_count': 0,
                        'percentage': 0.0
                    })

        return never_occurred[:10]

    def _find_least_occurred_combinations(self, match_patterns: Dict[int, Set[str]], matches: List[Match]) -> List[Dict[str, Any]]:
        total_matches = len(matches)
        combo_counts = Counter()

        for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
            for patterns in match_patterns.values():
                if len(patterns) < size:
                    continue
                for combo in combinations(patterns, size):
                    if self._valid_combination(combo):
                        combo_counts[combo] += 1

        least_occurred = []
        for combo, count in sorted(combo_counts.items(), key=lambda x: x[1])[:10]:
            pattern_details = [EventPatterns.get_pattern_by_name(name) for name in combo]
            percentage = (count / total_matches) * 100
            least_occurred.append({
                'events': [{'name': p.name, 'description': p.description} for p in pattern_details],
                'combination_size': len(combo),
                'occurrence_count': count,
                'percentage': percentage
            })
        return least_occurred

    def _find_most_occurred_combinations(self, match_patterns: Dict[int, Set[str]], matches: List[Match]) -> List[Dict[str, Any]]:
        total_matches = len(matches)
        combo_counts = Counter()

        for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
            for patterns in match_patterns.values():
                if len(patterns) < size:
                    continue
                for combo in combinations(patterns, size):
                    if self._valid_combination(combo):
                        combo_counts[combo] += 1

        most_occurred = []
        for combo, count in combo_counts.most_common(10):
            pattern_details = [EventPatterns.get_pattern_by_name(name) for name in combo]
            percentage = (count / total_matches) * 100
            most_occurred.append({
                'events': [{'name': p.name, 'description': p.description} for p in pattern_details],
                'combination_size': len(combo),
                'occurrence_count': count,
                'percentage': percentage
            })
        return most_occurred