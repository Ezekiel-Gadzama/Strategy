from datetime import datetime
from typing import List, Dict, Any, Set, Tuple
from itertools import combinations
from collections import defaultdict
import logging
import concurrent.futures
import threading
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
        self.combination_strategy = "by_event_type"  # "by_event_type", "by_market", "full"

        # Pre-organized patterns for faster access
        self._organize_patterns()

        # Threading
        self.thread_count = config.THREAD_COUNT

        # Global shared dictionary with thread lock
        self.global_combinations_dict = {}
        self.dict_lock = threading.Lock()

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

            # Reset global dictionary for each league/season
            self.global_combinations_dict = {}

            # Get all combinations analysis with optimized per-match approach
            all_combinations_analysis = self._analyze_matches_optimized(
                league_matches, league_id, season, league_name
            )

            league_results[f"{league_name}_{season}"] = all_combinations_analysis

        return league_results

    def _analyze_matches_optimized(self, matches: List[Match], league_id: int, season: int, league_name: str) -> Dict[
        str, Any]:
        """Optimized analysis using global shared dictionary - no combining needed!"""
        total_matches = len(matches)

        # Initialize results for this league/season
        self.results_manager.initialize_league_season(league_id, league_name, season, total_matches)

        print(f"🎯 Processing {total_matches} matches for {league_name} {season}")
        print(f"🔢 Combination sizes: {self.config.MIN_EVENTS_COMBINATION} to {self.config.MAX_EVENTS_COMBINATION}")

        # Process matches in batches using global dictionary
        batch_size = max(1, len(matches) // (self.thread_count * 2))

        batch_count = 0
        for batch_start in range(0, len(matches), batch_size):
            batch_count += 1
            batch_end = min(batch_start + batch_size, len(matches))
            match_batch = matches[batch_start:batch_end]

            print(f"\n📊 Processing batch {batch_count}: matches {batch_start}-{batch_end} of {len(matches)}")

            # Process this batch - all threads write to global dictionary
            self._process_batch_with_global_dict(match_batch)

            print(f"✅ Batch {batch_count} complete: {len(self.global_combinations_dict)} unique combinations so far")

        # No combining needed - we already have the final results in global_combinations_dict!
        print(f"\n🎉 All batches processed")
        valid_combinations_count = sum(self.global_combinations_dict.values())

        # Convert string keys back to tuples for final processing
        final_combinations_with_tuples = {}
        for combo_key, count in self.global_combinations_dict.items():
            combo_tuple = tuple(combo_key.split("|"))
            final_combinations_with_tuples[combo_tuple] = count

        # Save final results for this league/season - USE THE LAZY VERSION
        final_results = self._prepare_final_results_lazy(final_combinations_with_tuples, total_matches,
                                                         valid_combinations_count)
        self.results_manager.save_analysis_results(league_id, season, final_results)

        print(f"🎉 Analysis complete for {league_name} {season}")
        print(f"📊 Found {len(self.global_combinations_dict)} unique combinations across {total_matches} matches")

        return final_results

    def _process_batch_with_global_dict(self, matches: List[Match]):
        """Process a batch with all threads writing to global dictionary"""
        # Split batch for threading
        sub_batches = [matches[i:i + max(1, len(matches) // self.thread_count)]
                       for i in range(0, len(matches), max(1, len(matches) // self.thread_count))]

        with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count) as executor:
            # Submit all sub-batches - they all write to the global dictionary
            futures = [
                executor.submit(self._analyze_match_batch_global, sub_batch)
                for sub_batch in sub_batches if sub_batch
            ]

            # Wait for all to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()  # Just wait for completion - results are in global dict
                except Exception as e:
                    self.logger.error(f"Error processing sub-batch: {e}")
                    import traceback
                    self.logger.error(f"Detailed error: {traceback.format_exc()}")

    def _analyze_match_batch_global(self, matches: List[Match]):
        """Analyze a batch of matches and write directly to global dictionary"""
        # Local batch dictionary to reduce lock contention
        local_batch_dict = {}

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

                # Count each combination in local batch dictionary
                for combo in combinations_for_match:
                    combo_key = "|".join(combo)  # Convert tuple to string
                    local_batch_dict[combo_key] = local_batch_dict.get(combo_key, 0) + 1

        # Merge local batch results into global dictionary (with lock)
        with self.dict_lock:
            for combo_key, count in local_batch_dict.items():
                self.global_combinations_dict[combo_key] = self.global_combinations_dict.get(combo_key, 0) + count

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

    def _process_combination_list(self, combinations: List[Tuple[Tuple[str, ...], int]], total_matches: int) -> List[
        Dict]:
        """Process a list of combinations into display-ready result items"""
        processed = []
        for combo, count in combinations:
            pattern_details = []
            for name in combo:
                if name in self.pattern_name_to_obj:
                    pattern = self.pattern_name_to_obj[name]
                    pattern_details.append({
                        'name': pattern.name,
                        'description': pattern.description,
                        'event_type': pattern.event_type.value,
                        'market': pattern.market
                    })

            processed.append({
                'events': pattern_details,
                'combination_size': len(combo),
                'occurrence_count': count,
                'percentage': (count / total_matches) * 100 if total_matches > 0 else 0.0,
                'strategy': self.combination_strategy
            })

        return processed

    def _prepare_final_results_lazy(self, combinations_dict: Dict[Tuple[str, ...], int], total_matches: int,
                                    valid_combinations_count: int) -> Dict[str, Any]:
        """Only process combinations that will be displayed in results - optimized version"""
        # Group by size first
        combinations_by_size = defaultdict(list)
        for combo, count in combinations_dict.items():
            combinations_by_size[len(combo)].append((combo, count))

        organized_results = {}
        all_occurred_candidates = []  # Store candidate combinations, not processed items
        all_never_occurred_candidates = []

        for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
            if size not in combinations_by_size:
                organized_results[size] = self._get_empty_size_results()
                continue

            size_combinations = combinations_by_size[size]

            # Split into occurred and never occurred
            occurred_combos = [(combo, count) for combo, count in size_combinations if count > 0]
            never_occurred_combos = [(combo, count) for combo, count in size_combinations if count == 0]

            # For occurred: only process the extremes (least and most occurred)
            occurred_candidates = self._get_display_candidates(occurred_combos)

            # For never occurred: only process up to display limit
            never_occurred_candidates = never_occurred_combos[:self.config.MAX_RESULTS_PER_CATEGORY]

            # Process only the candidates
            processed_occurred = self._process_combination_list(occurred_candidates, total_matches)
            processed_never_occurred = self._process_combination_list(never_occurred_candidates, total_matches)

            # Sort occurred combinations for final selection
            processed_occurred_sorted = sorted(processed_occurred, key=lambda x: x['occurrence_count'])

            organized_results[size] = {
                'never_occurred': processed_never_occurred[:self.config.MAX_RESULTS_PER_CATEGORY],
                'least_occurred': processed_occurred_sorted[:self.config.MAX_RESULTS_PER_CATEGORY],
                'most_occurred': list(reversed(processed_occurred_sorted[-self.config.MAX_RESULTS_PER_CATEGORY:])),
                'total_combinations': len(size_combinations),
                'occurred_count': len(occurred_combos),
                'never_occurred_count': len(never_occurred_combos)
            }

            # Store candidates for overall stats (we'll process them later if needed)
            all_occurred_candidates.extend(occurred_candidates)
            all_never_occurred_candidates.extend(never_occurred_candidates)

        # Calculate stats using raw counts to avoid expensive processing
        stats = self._calculate_stats_from_raw(all_occurred_candidates, all_never_occurred_candidates, total_matches)

        # For the final display arrays, we need to process a small subset
        overall_occurred = self._process_combination_list(
            self._get_overall_display_candidates(all_occurred_candidates),
            total_matches
        )
        overall_never_occurred = self._process_combination_list(
            all_never_occurred_candidates[:self.config.MAX_RESULTS_PER_CATEGORY],
            total_matches
        )

        return {
            'organized_results': organized_results,
            'never_occurred': overall_never_occurred[:self.config.MAX_RESULTS_PER_CATEGORY],
            'least_occurred': overall_occurred[:self.config.MAX_RESULTS_PER_CATEGORY],
            'most_occurred': overall_occurred[-self.config.MAX_RESULTS_PER_CATEGORY:],
            'stats': stats
        }

    def _get_display_candidates(self, combinations: List[Tuple[Tuple[str, ...], int]]) -> List[
        Tuple[Tuple[str, ...], int]]:
        """Get candidate combinations for display (extremes only)"""
        if not combinations:
            return []

        # Sort by occurrence count to find extremes
        combinations_sorted = sorted(combinations, key=lambda x: x[1])

        max_display = self.config.MAX_RESULTS_PER_CATEGORY
        # Take candidates from both ends (least and most occurred)
        candidates = (combinations_sorted[:max_display] +  # Least occurred
                      combinations_sorted[-max_display:])  # Most occurred

        # Remove duplicates and return
        return list(dict.fromkeys(candidates))  # Preserves order while removing duplicates

    def _get_overall_display_candidates(self, combinations: List[Tuple[Tuple[str, ...], int]]) -> List[
        Tuple[Tuple[str, ...], int]]:
        """Get overall display candidates across all sizes"""
        if not combinations:
            return []

        # Sort by occurrence count
        combinations_sorted = sorted(combinations, key=lambda x: x[1])

        max_display = self.config.MAX_RESULTS_PER_CATEGORY * 2  # Get enough for both least and most
        # Take from both extremes
        candidates = (combinations_sorted[:max_display] +  # Least occurred
                      combinations_sorted[-max_display:])  # Most occurred

        return list(dict.fromkeys(candidates))

    def _calculate_stats_from_raw(self, occurred_candidates: List[Tuple[Tuple[str, ...], int]],
                                  never_occurred_candidates: List[Tuple[Tuple[str, ...], int]],
                                  total_matches: int) -> Dict:
        """Calculate statistics from raw combination data (no processing needed)"""
        if not occurred_candidates:
            return {
                'total_combinations_checked': len(occurred_candidates) + len(never_occurred_candidates),
                'valid_combinations_count': 0,
                'never_occurred_count': len(never_occurred_candidates),
                'occurred_count': 0,
                'min_occurrence': 0,
                'max_occurrence': 0,
                'avg_occurrence': 0
            }

        # Extract just the counts for statistics
        occurrences = [count for _, count in occurred_candidates]
        return {
            'total_combinations_checked': len(occurred_candidates) + len(never_occurred_candidates),
            'valid_combinations_count': sum(occurrences),
            'never_occurred_count': len(never_occurred_candidates),
            'occurred_count': len(occurred_candidates),
            'min_occurrence': min(occurrences),
            'max_occurrence': max(occurrences),
            'avg_occurrence': sum(occurrences) / len(occurred_candidates)
        }

    def _get_empty_size_results(self) -> Dict[str, Any]:
        """Return empty results structure for a size with no combinations"""
        return {
            'never_occurred': [],
            'least_occurred': [],
            'most_occurred': [],
            'total_combinations': 0,
            'occurred_count': 0,
            'never_occurred_count': 0
        }