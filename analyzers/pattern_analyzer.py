from typing import List, Dict, Any, Tuple
from itertools import combinations
from collections import defaultdict
import logging
import concurrent.futures
import threading
from data.models import Match
from patterns.event_patterns import EventPatterns
from config.settings import AnalysisConfig
from utils.results_manager import ResultsManager
from utils.odds_calculator import OddsCalculator


class PatternAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.all_patterns = EventPatterns.get_all_patterns()
        self.results_manager = ResultsManager()

        # Initialize odds calculator
        self.odds_calculator = OddsCalculator()
        # Toggle whether to use odds info in analysis
        self.use_odd_info = True  # 👈 Added flag
        self.max_length = 0

        print(f"length of pattern: {len(self.all_patterns)}")

        # Strategy options
        self.combination_strategy = "full"  # "by_event_type", "by_market", "full"

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

    # -------------------------------------------------------------------------
    # --- ODDS HANDLING (conditional on self.use_odd_info)
    # -------------------------------------------------------------------------
    def _calculate_combination_odds(self, league_id: int, season: int,
                                    combination: Tuple[str, ...],
                                    occurrence_count: int,
                                    total_matches: int) -> Dict[str, Any]:
        """Calculate odds for a combination (conditionally uses odds info)"""
        occurrence_probability = (occurrence_count / total_matches) * 100 if total_matches > 0 else 0.0

        if not self.use_odd_info:
            # 🔕 Skip odds calculations entirely
            return {
                "odds_calculated": False,
                "implied_probability": occurrence_probability,
                "combined_odds": None,
                "expected_value": None
            }

        # ✅ Only run if odds are enabled
        self.odds_calculator.get_latest_match_odds(league_id, season)
        odds_result = self.odds_calculator.calculate_combination_odds(
            combination, occurrence_probability
        )

        odds_result["odds_calculated"] = True
        return odds_result

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
                                                         valid_combinations_count, league_id, season)
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

    # -------------------------------------------------------------------------
    # --- COMBINATION PROCESSING (unchanged except odds condition)
    # -------------------------------------------------------------------------
    def _process_combination_list(self, combinations: List[Tuple[Tuple[str, ...], int]],
                                  total_matches: int, league_id: int, season: int) -> List[Dict]:
        """Process a list of combinations into display-ready result items (odds optional)"""
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

            # ⚙️ Conditionally include odds info
            if self.use_odd_info:
                odds_info = self._calculate_combination_odds(league_id, season, combo, count, total_matches)
            else:
                odds_info = None

            processed.append({
                'events': pattern_details,
                'combination_size': len(combo),
                'occurrence_count': count,
                'percentage': (count / total_matches) * 100 if total_matches > 0 else 0.0,
                'strategy': self.combination_strategy,
                'odds_info': odds_info
            })

        return processed

    def _prepare_final_results_lazy(
        self,
        combinations_dict: Dict[Tuple[str, ...], int],
        total_matches: int,
        valid_combinations_count: int,
        league_id: int,
        season: int
    ) -> Dict[str, Any]:
        """Prepare final results. Behavior depends on use_odd_info mode:
           - Normal mode: top/bottom by occurrence
           - Odds mode: top/bottom by value bet % (and tie-break by frequency)
        """
        combinations_by_size = defaultdict(list)
        for combo, count in combinations_dict.items():
            combinations_by_size[len(combo)].append((combo, count))

        organized_results = {}
        all_occurred_candidates = []
        all_never_occurred_candidates = []

        # ------------------------------------------------------------------
        # --- NORMAL (pattern-frequency) MODE -------------------------------
        # ------------------------------------------------------------------
        if not self.use_odd_info:
            for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
                if size not in combinations_by_size:
                    organized_results[size] = self._get_empty_size_results()
                    continue

                size_combinations = combinations_by_size[size]

                occurred_combos = [(combo, count) for combo, count in size_combinations if count > 0]
                never_occurred_combos = [(combo, count) for combo, count in size_combinations if count == 0]

                occurred_candidates = self._get_display_candidates(occurred_combos)
                never_occurred_candidates = never_occurred_combos[:self.config.MAX_RESULTS_PER_CATEGORY]

                processed_occurred = self._process_combination_list(
                    occurred_candidates, total_matches, league_id, season
                )
                processed_never_occurred = self._process_combination_list(
                    never_occurred_candidates, total_matches, league_id, season
                )

                processed_occurred_sorted = sorted(processed_occurred, key=lambda x: x["occurrence_count"])
                max_display = self.config.MAX_RESULTS_PER_CATEGORY
                if self.use_odd_info:
                    max_display = len(processed_occurred_sorted)

                organized_results[size] = {
                    "never_occurred": processed_never_occurred[: self.config.MAX_RESULTS_PER_CATEGORY],
                    "least_occurred": processed_occurred_sorted[: max_display],
                    "most_occurred": list(
                        reversed(processed_occurred_sorted[-max_display:])
                    ),
                    "total_combinations": len(size_combinations),
                    "occurred_count": len(occurred_combos),
                    "never_occurred_count": len(never_occurred_combos),
                }

                all_occurred_candidates.extend(occurred_candidates)
                all_never_occurred_candidates.extend(never_occurred_candidates)

            stats = self._calculate_stats_from_raw(all_occurred_candidates, all_never_occurred_candidates, total_matches)

            overall_occurred = self._process_combination_list(
                self._get_overall_display_candidates(all_occurred_candidates),
                total_matches,
                league_id,
                season,
            )
            overall_never_occurred = self._process_combination_list(
                all_never_occurred_candidates[: self.config.MAX_RESULTS_PER_CATEGORY],
                total_matches,
                league_id,
                season,
            )
            max_display = self.config.MAX_RESULTS_PER_CATEGORY
            if self.use_odd_info:
                max_display = len(overall_occurred)
            return {
                "organized_results": organized_results,
                "never_occurred": overall_never_occurred[: self.config.MAX_RESULTS_PER_CATEGORY],
                "least_occurred": overall_occurred[: max_display],
                "most_occurred": overall_occurred[-max_display:],
                "stats": stats,
            }

        # ------------------------------------------------------------------
        # --- ODDS (VALUE BET) MODE ----------------------------------------
        # ------------------------------------------------------------------
        else:
            print("💰 Running in VALUE BET mode (use_odd_info=True)")

            value_results = []
            for size, size_combos in combinations_by_size.items():
                # process all to include odds info
                processed = self._process_combination_list(size_combos, total_matches, league_id, season)
                value_results.extend(processed)

            # filter only combos that have valid positive value bets
            valuable = [
                combo
                for combo in value_results
                if combo.get("odds_info")
                and combo["odds_info"].get("is_valuable", False)
                and combo["odds_info"].get("value_indicator", 0) > 0
            ]

            if not valuable:
                print("⚠️ No value bets found in this dataset.")
                return {"organized_results": {}, "most_valuable": [], "least_valuable": [], "stats": {}}

            # sort by value indicator (highest first)
            valuable.sort(
                key=lambda x: (
                    x["odds_info"].get("value_indicator", 0),
                    x["occurrence_count"],  # tie-breaker by frequency
                ),
                reverse=True,
            )

            # top 20 highest-value bets

            max_display = self.config.MAX_RESULTS_PER_CATEGORY
            if self.use_odd_info:
                max_display = len(valuable)

            most_valuable = valuable[: max_display]

            # bottom 20 lowest-value (but still >0) bets
            least_valuable = sorted(
                valuable, key=lambda x: (x["odds_info"].get("value_indicator", 0), -x["occurrence_count"])
            )[: max_display]

            return {
                "organized_results": {},
                "most_valuable": most_valuable,
                "least_valuable": least_valuable,
                "stats": {
                    "total_value_bets": len(valuable),
                    "highest_value": most_valuable[0]["odds_info"]["value_indicator"],
                    "lowest_value": least_valuable[0]["odds_info"]["value_indicator"],
                },
            }

    def _get_display_candidates(self, combinations: List[Tuple[Tuple[str, ...], int]]) -> List[
        Tuple[Tuple[str, ...], int]]:
        """Get candidate combinations for display (extremes only)"""
        if not combinations:
            return []

        # Sort by occurrence count to find extremes
        combinations_sorted = sorted(combinations, key=lambda x: x[1])

        max_display = self.config.MAX_RESULTS_PER_CATEGORY
        if self.use_odd_info:
            max_display = len(combinations_sorted)

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
        if self.use_odd_info:
            max_display = len(combinations_sorted)

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