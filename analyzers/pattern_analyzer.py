from datetime import datetime
from typing import List, Dict, Any, Set, Tuple
from itertools import combinations
from collections import defaultdict, Counter
import logging
import concurrent.futures
from data.models import Match
from patterns.event_patterns import EventPatterns
from config.settings import AnalysisConfig
from utils.results_manager import ResultsManager

class PatternAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.all_patterns = EventPatterns.get_all_patterns()
        self.results_manager = ResultsManager()

        print(f"length of pattern: {len(self.all_patterns)}")

        # Strategy options
        self.combination_strategy = "by_event_type"

        # Pre-organized patterns for faster access
        self._organize_patterns()

        # Threading
        self.thread_count = config.THREAD_COUNT

    def _organize_patterns(self):
        """Organize patterns in hierarchical structure for efficient combination generation"""
        self.patterns_by_event_type = defaultdict(list)
        self.patterns_by_market = defaultdict(lambda: defaultdict(list))
        self.all_pattern_names = []
        self.pattern_name_to_obj = {}

        for pattern in self.all_patterns:
            self.patterns_by_event_type[pattern.event_type].append(pattern)
            self.patterns_by_market[pattern.event_type][pattern.market].append(pattern)
            self.all_pattern_names.append(pattern.name)
            self.pattern_name_to_obj[pattern.name] = pattern

        self.logger.info(
            f"Organized {len(self.all_patterns)} patterns into {len(self.patterns_by_event_type)} event types")

    def analyze_matches(self, matches: List[Match]) -> Dict[str, Any]:
        """Analyze matches league by league with comprehensive tracking"""
        leagues = set((m.league, m.league_id, m.season) for m in matches)
        league_results = {}

        for league_name, league_id, season in leagues:
            league_matches = [m for m in matches if
                              m.league == league_name and m.league_id == league_id and m.season == season]
            self.logger.info(f"Analyzing {len(league_matches)} matches in {league_name} ({season})")
            print(f"🚀 Starting analysis for {league_name} {season} with {len(league_matches)} matches")

            # Get all combinations analysis with optimized per-match approach
            all_combinations_analysis = self._analyze_matches_optimized(
                league_matches, league_id, season, league_name
            )

            league_results[f"{league_name}_{season}"] = all_combinations_analysis

        return league_results

    def _analyze_matches_optimized(self, matches: List[Match], league_id: int, season: int, league_name: str) -> Dict[
        str, Any]:
        """Optimized analysis that processes each batch independently and combines at the end"""
        total_matches = len(matches)

        # Initialize results for this league/season
        self.results_manager.initialize_league_season(league_id, league_name, season, total_matches)

        print(f"🎯 Processing {total_matches} matches for {league_name} {season}")
        print(f"🔢 Combination sizes: {self.config.MIN_EVENTS_COMBINATION} to {self.config.MAX_EVENTS_COMBINATION}")

        # Process matches in batches for threading
        batch_size = max(1, len(matches) // (self.thread_count * 2))
        all_batch_results = []  # Store results from each batch

        batch_count = 0
        for batch_start in range(0, len(matches), batch_size):
            batch_count += 1
            batch_end = min(batch_start + batch_size, len(matches))
            match_batch = matches[batch_start:batch_end]

            print(f"\n📊 Processing batch {batch_count}: matches {batch_start}-{batch_end} of {len(matches)}")

            # Process this batch independently
            batch_result = self._process_batch_independently(match_batch)
            all_batch_results.append(batch_result)

            print(f"✅ Batch {batch_count} complete: {len(batch_result)} unique combinations found")

        # Combine all batch results at the end
        print(f"\n🔗 Combining results from {len(all_batch_results)} batches...")
        final_combinations_counter = self._combine_batch_results(all_batch_results)
        valid_combinations_count = sum(final_combinations_counter.values())

        # Save final results for this league/season
        final_results = self._prepare_final_results(final_combinations_counter, total_matches, valid_combinations_count)
        self.results_manager.save_analysis_results(league_id, season, final_results)

        print(f"🎉 Analysis complete for {league_name} {season}")
        print(f"📊 Found {len(final_combinations_counter)} unique combinations across {total_matches} matches")

        return final_results

    def _process_batch_independently(self, matches: List[Match]) -> Dict[Tuple[str, ...], int]:
        """Process a batch of matches independently and return combination counts"""
        # Split batch for threading
        sub_batches = [matches[i:i + max(1, len(matches) // self.thread_count)]
                       for i in range(0, len(matches), max(1, len(matches) // self.thread_count))]

        batch_combinations = Counter()

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            future_to_batch = {
                executor.submit(self._analyze_match_batch, sub_batch): sub_batch
                for sub_batch in sub_batches if sub_batch
            }

            for future in concurrent.futures.as_completed(future_to_batch):
                try:
                    sub_batch_result = future.result()
                    # Combine sub-batch results into main batch counter
                    for combo, count in sub_batch_result.items():
                        batch_combinations[combo] += count
                except Exception as e:
                    self.logger.error(f"Error processing sub-batch: {e}")

        return batch_combinations

    def _combine_batch_results(self, all_batch_results: List[Dict[Tuple[str, ...], int]]) -> Counter:
        """Combine results from all batches into a single counter"""
        final_counter = Counter()

        for batch_result in all_batch_results:
            for combo, count in batch_result.items():
                final_counter[combo] += count

        return final_counter

    def _analyze_match_batch(self, matches: List[Match]) -> Dict[Tuple[str, ...], int]:
        """Analyze a batch of matches and return combination counts"""
        batch_combinations = Counter()

        for match in matches:
            # Get patterns that occurred in this specific match
            occurring_patterns = self._get_occurring_patterns_for_match(match)

            if not occurring_patterns:
                continue

            # Generate combinations only from patterns that actually occurred
            for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
                if len(occurring_patterns) < size:
                    continue

                # Generate combinations using the selected strategy
                combinations_for_match = self._generate_valid_combinations(occurring_patterns, size)

                # Count each combination for this match
                for combo in combinations_for_match:
                    batch_combinations[combo] += 1

        return batch_combinations

    def _get_occurring_patterns_for_match(self, match: Match) -> List[str]:
        """Get list of pattern names that occurred in this specific match"""
        occurring_patterns = []

        for pattern in self.all_patterns:
            try:
                if pattern.condition(match):
                    occurring_patterns.append(pattern.name)
            except Exception as e:
                self.logger.debug(f"Error evaluating pattern {pattern.name} for match {match.id}: {e}")
                continue

        return occurring_patterns

    def _generate_valid_combinations(self, occurring_patterns: List[str], size: int) -> List[Tuple[str, ...]]:
        """Generate valid combinations based on strategy from occurring patterns"""
        if self.combination_strategy == "by_event_type":
            return self._generate_combinations_by_event_type_from_occurring(occurring_patterns, size)
        elif self.combination_strategy == "by_market":
            return self._generate_combinations_by_market_from_occurring(occurring_patterns, size)
        else:  # full
            return self._generate_full_combinations_from_occurring(occurring_patterns, size)

    def _generate_combinations_by_event_type_from_occurring(self, occurring_patterns: List[str], size: int) -> List[
        Tuple[str, ...]]:
        """Generate combinations by event type from occurring patterns only"""
        # Group occurring patterns by event type
        patterns_by_type = defaultdict(list)
        for pattern_name in occurring_patterns:
            pattern = self.pattern_name_to_obj.get(pattern_name)
            if pattern:
                patterns_by_type[pattern.event_type].append(pattern_name)

        # Get event types that have occurring patterns
        available_event_types = list(patterns_by_type.keys())

        if size > len(available_event_types):
            return []

        valid_combinations = []

        # Generate combinations of event types
        for event_type_combo in combinations(available_event_types, size):
            # Get patterns for each event type in the combination
            pattern_choices = [patterns_by_type[event_type] for event_type in event_type_combo]

            # Generate all combinations across the chosen event types
            for pattern_names in self._product(*pattern_choices):
                valid_combinations.append(tuple(pattern_names))

        return valid_combinations

    def _generate_combinations_by_market_from_occurring(self, occurring_patterns: List[str], size: int) -> List[
        Tuple[str, ...]]:
        """Generate combinations by market from occurring patterns only"""
        # Group occurring patterns by market
        patterns_by_market = defaultdict(list)
        for pattern_name in occurring_patterns:
            pattern = self.pattern_name_to_obj.get(pattern_name)
            if pattern:
                patterns_by_market[pattern.market].append(pattern_name)

        # Get markets that have occurring patterns
        available_markets = list(patterns_by_market.keys())

        if size > len(available_markets):
            return []

        valid_combinations = []

        # Generate combinations of markets
        for market_combo in combinations(available_markets, size):
            # Get patterns for each market in the combination
            pattern_choices = [patterns_by_market[market] for market in market_combo]

            # Generate all combinations across the chosen markets
            for pattern_names in self._product(*pattern_choices):
                valid_combinations.append(tuple(pattern_names))

        return valid_combinations

    def _generate_full_combinations_from_occurring(self, occurring_patterns: List[str], size: int) -> List[
        Tuple[str, ...]]:
        """Generate all combinations from occurring patterns only"""
        if size > len(occurring_patterns):
            return []

        return list(combinations(occurring_patterns, size))

    def _product(self, *args):
        """Custom product function to handle empty lists"""
        if not args:
            yield ()
            return

        first, rest = args[0], args[1:]
        for item in first:
            for product_rest in self._product(*rest):
                yield (item,) + product_rest

    def _prepare_final_results(self, combinations_counter: Counter, total_matches: int,
                               valid_combinations_count: int) -> Dict[str, Any]:
        """Prepare final results from the combinations counter"""
        never_occurred = []
        occurred = []

        for combo, count in combinations_counter.items():
            pattern_details = [self.pattern_name_to_obj[name] for name in combo if name in self.pattern_name_to_obj]

            result_item = {
                'events': [{'name': p.name, 'description': p.description,
                            'event_type': p.event_type.value, 'market': p.market}
                           for p in pattern_details],
                'combination_size': len(combo),
                'occurrence_count': count,
                'percentage': (count / total_matches) * 100 if total_matches > 0 else 0.0,
                'strategy': self.combination_strategy
            }

            if count == 0:
                never_occurred.append(result_item)
            else:
                occurred.append(result_item)

        # Sort occurred combinations
        occurred_sorted = sorted(occurred, key=lambda x: x['occurrence_count'])

        stats = {
            'total_combinations_checked': len(combinations_counter),
            'valid_combinations_count': valid_combinations_count,
            'never_occurred_count': len(never_occurred),
            'occurred_count': len(occurred),
            'min_occurrence': min([x['occurrence_count'] for x in occurred]) if occurred else 0,
            'max_occurrence': max([x['occurrence_count'] for x in occurred]) if occurred else 0,
            'avg_occurrence': sum([x['occurrence_count'] for x in occurred]) / len(occurred) if occurred else 0
        }

        return {
            'never_occurred': never_occurred[:self.config.MAX_RESULTS_PER_CATEGORY],
            'least_occurred': occurred_sorted[:self.config.MAX_RESULTS_PER_CATEGORY],
            'most_occurred': list(reversed(occurred_sorted[-self.config.MAX_RESULTS_PER_CATEGORY:])),
            'stats': stats
        }