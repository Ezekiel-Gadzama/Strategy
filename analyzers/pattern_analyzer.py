from typing import List, Dict, Any, Set, Tuple
from itertools import combinations, product, islice
from collections import Counter, defaultdict
import logging
import concurrent.futures
import threading
from data.models import Match
from patterns.event_patterns import EventPatterns, EventCondition
from config.settings import AnalysisConfig
from utils.progress_manager import ProgressManager


class PatternAnalyzer:
    def __init__(self, config: AnalysisConfig):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.all_patterns = EventPatterns.get_all_patterns()
        self.progress_manager = ProgressManager()

        print(f"length of pattern: {len(self.all_patterns)}")

        # Strategy options
        self.combination_strategy = "by_event_type"

        # Pre-organized patterns for faster access
        self._organize_patterns()

        # Threading
        self.thread_count = config.THREAD_COUNT
        self.combination_lock = threading.Lock()

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

    def set_combination_strategy(self, strategy: str):
        """Set the combination strategy"""
        valid_strategies = ["by_event_type", "by_market", "full"]
        if strategy not in valid_strategies:
            raise ValueError(f"Strategy must be one of {valid_strategies}")
        self.combination_strategy = strategy
        self.logger.info(f"Combination strategy set to: {strategy}")

    def analyze_matches(self, matches: List[Match]) -> Dict[str, Any]:
        """Analyze matches league by league with optimized combination checking"""
        leagues = set((m.league, m.league_id, m.season) for m in matches)
        league_results = {}

        # Precompute match patterns for all matches
        all_match_patterns = self._find_match_patterns(matches)

        for league_name, league_id, season in leagues:
            league_matches = [m for m in matches if
                              m.league == league_name and m.league_id == league_id and m.season == season]
            self.logger.info(f"Analyzing {len(league_matches)} matches in {league_name} ({season})")

            # Filter match patterns for this league
            league_match_patterns = {match_id: patterns for match_id, patterns in all_match_patterns.items()
                                     if any(m.id == match_id and m.league == league_name for m in league_matches)}

            # Get all combinations analysis with optimization
            all_combinations_analysis = self._analyze_all_combinations_optimized(league_match_patterns, league_matches,
                                                                                 league_id, season)

            league_results[f"{league_name}_{season}"] = {
                'never_occurred': all_combinations_analysis['never_occurred'],
                'least_occurred': all_combinations_analysis['least_occurred'],
                'most_occurred': all_combinations_analysis['most_occurred'],
                'total_matches': len(league_matches),
                'total_patterns_analyzed': len(self.all_patterns),
                'combination_strategy': self.combination_strategy,
                'stats': all_combinations_analysis['stats']
            }

        return league_results

    def _find_match_patterns(self, matches: List[Match]) -> Dict[int, Set[str]]:
        """Find which patterns occur in each match"""
        match_patterns = {}

        for match in matches:
            occurring_patterns = set()
            for pattern in self.all_patterns:
                try:
                    if pattern.condition(match):
                        occurring_patterns.add(pattern.name)
                except Exception as e:
                    self.logger.debug(f"Error evaluating pattern {pattern.name}: {e}")
                    continue
            match_patterns[match.id] = occurring_patterns

        self.logger.info(f"Found patterns for {len(match_patterns)} matches")
        return match_patterns

    def _generate_combinations_by_strategy(self, size: int) -> List[Tuple[str]]:
        """Generate combinations based on the selected strategy"""
        if self.combination_strategy == "by_event_type":
            return self._generate_combinations_by_event_type(size)
        elif self.combination_strategy == "by_market":
            return self._generate_combinations_by_market(size)
        else:  # full
            return self._generate_full_combinations(size)

    def _generate_combinations_by_event_type(self, size: int) -> List[Tuple[str]]:
        """Generate combinations picking one pattern from each EventType"""
        event_types = list(self.patterns_by_event_type.keys())

        if size > len(event_types):
            self.logger.warning(f"Requested size {size} exceeds available event types {len(event_types)}")
            return []

        all_combinations = []

        for event_type_combo in combinations(event_types, size):
            pattern_choices = []
            for event_type in event_type_combo:
                patterns_in_type = [p.name for p in self.patterns_by_event_type[event_type]]
                pattern_choices.append(patterns_in_type)

            for pattern_combo in product(*pattern_choices):
                all_combinations.append(pattern_combo)

        self.logger.info(f"Generated {len(all_combinations)} combinations of size {size} by event type")
        return all_combinations

    def _generate_combinations_by_market(self, size: int) -> List[Tuple[str]]:
        """Generate combinations picking one pattern from each market"""
        all_markets = set()
        market_to_patterns = defaultdict(list)

        for event_type, markets in self.patterns_by_market.items():
            for market, patterns in markets.items():
                all_markets.add(market)
                for pattern in patterns:
                    market_to_patterns[market].append(pattern.name)

        if size > len(all_markets):
            self.logger.warning(f"Requested size {size} exceeds available markets {len(all_markets)}")
            return []

        all_combinations = []

        for market_combo in combinations(all_markets, size):
            pattern_choices = []
            for market in market_combo:
                patterns_in_market = market_to_patterns[market]
                pattern_choices.append(patterns_in_market)

            for pattern_combo in product(*pattern_choices):
                all_combinations.append(pattern_combo)

        self.logger.info(f"Generated {len(all_combinations)} combinations of size {size} by market")
        return all_combinations

    def _generate_full_combinations(self, size: int) -> List[Tuple[str]]:
        """Generate all possible combinations without restrictions"""
        if size > len(self.all_pattern_names):
            return []

        all_combinations = list(combinations(self.all_pattern_names, size))
        self.logger.info(f"Generated {len(all_combinations)} full combinations of size {size}")
        return all_combinations

    def _valid_combination(self, combo: Tuple[str]) -> bool:
        """Validate combination based on strategy"""
        if self.combination_strategy == "by_event_type":
            return self._valid_combination_by_event_type(combo)
        elif self.combination_strategy == "by_market":
            return self._valid_combination_by_market(combo)
        else:  # full
            return True

    def _valid_combination_by_event_type(self, combo: Tuple[str]) -> bool:
        """Ensure patterns come from different event types"""
        event_types_seen = set()
        for name in combo:
            pattern = self.pattern_name_to_obj.get(name)
            if pattern is None:
                return False
            if pattern.event_type in event_types_seen:
                return False
            event_types_seen.add(pattern.event_type)
        return True

    def _valid_combination_by_market(self, combo: Tuple[str]) -> bool:
        """Ensure patterns come from different markets"""
        markets_seen = set()
        for name in combo:
            pattern = self.pattern_name_to_obj.get(name)
            if pattern is None:
                return False
            if pattern.market in markets_seen:
                return False
            markets_seen.add(pattern.market)
        return True

    def _analyze_combination_batch(self, combinations_batch: List[Tuple[str]], match_patterns: Dict[int, Set[str]],
                                   total_matches: int) -> Dict[str, List]:
        """Analyze a batch of combinations (for threading)"""
        batch_results = {
            'never_occurred': [],
            'occurred': []
        }

        for combo in combinations_batch:
            if not self._valid_combination(combo):
                continue

            # Count occurrences for this combination
            occurred_count = 0
            for patterns in match_patterns.values():
                if set(combo).issubset(patterns):
                    occurred_count += 1

            pattern_details = [self.pattern_name_to_obj[name] for name in combo]
            result_item = {
                'events': [{'name': p.name, 'description': p.description,
                            'event_type': p.event_type.value, 'market': p.market}
                           for p in pattern_details],
                'combination_size': len(combo),
                'occurrence_count': occurred_count,
                'percentage': (occurred_count / total_matches) * 100 if total_matches > 0 else 0.0,
                'strategy': self.combination_strategy
            }

            if occurred_count == 0:
                batch_results['never_occurred'].append(result_item)
            else:
                batch_results['occurred'].append(result_item)

        return batch_results

    def _analyze_all_combinations_optimized(self, match_patterns: Dict[int, Set[str]], matches: List[Match],
                                            league_id: int, season: int) -> Dict[str, Any]:
        """Optimized combination analysis with threading and progress tracking"""
        total_matches = len(matches)
        all_never_occurred = []
        all_occurred = []

        total_combinations_checked = 0
        valid_combinations_count = 0

        # Analyze all combinations across all sizes
        for size in range(self.config.MIN_EVENTS_COMBINATION, self.config.MAX_EVENTS_COMBINATION + 1):
            self.logger.info(f"🔍 Analyzing combinations of size {size} for league {league_id}, season {season}")

            combinations_to_check = self._generate_combinations_by_strategy(size)
            if not combinations_to_check:
                continue

            total_combinations_checked += len(combinations_to_check)

            # Check for resume point
            resume_combo = self.progress_manager.get_resume_point(league_id, season, size)
            start_index = 0

            if resume_combo:
                try:
                    start_index = combinations_to_check.index(resume_combo)
                    self.logger.info(f"Resuming from combination {resume_combo} at index {start_index}")
                except ValueError:
                    self.logger.info("Resume combination not found, starting from beginning")

            # Process combinations in batches for threading
            batch_size = max(1, len(combinations_to_check) // (self.thread_count * 10))

            for batch_start in range(start_index, len(combinations_to_check), batch_size):
                batch_end = min(batch_start + batch_size, len(combinations_to_check))
                batch = combinations_to_check[batch_start:batch_end]

                # Split batch for threading
                sub_batches = [batch[i:i + max(1, len(batch) // self.thread_count)]
                               for i in range(0, len(batch), max(1, len(batch) // self.thread_count))]

                with concurrent.futures.ThreadPoolExecutor(max_workers=self.thread_count) as executor:
                    future_to_batch = {
                        executor.submit(self._analyze_combination_batch, sub_batch, match_patterns,
                                        total_matches): sub_batch
                        for sub_batch in sub_batches if sub_batch
                    }

                    for future in concurrent.futures.as_completed(future_to_batch):
                        try:
                            batch_result = future.result()
                            all_never_occurred.extend(batch_result['never_occurred'])
                            all_occurred.extend(batch_result['occurred'])
                            valid_combinations_count += len(batch_result['never_occurred']) + len(
                                batch_result['occurred'])

                        except Exception as e:
                            self.logger.error(f"Error processing batch: {e}")

                # Save progress after each batch
                if batch_end < len(combinations_to_check):
                    next_combo = combinations_to_check[batch_end] if batch_end < len(combinations_to_check) else batch[
                        -1]
                    self.progress_manager.save_progress(
                        league_id, season, size, next_combo,
                        len(combinations_to_check), batch_end
                    )

        # Sort occurred combinations by count
        all_occurred_sorted = sorted(all_occurred, key=lambda x: x['occurrence_count'])

        # Prepare statistics
        stats = {
            'total_combinations_checked': total_combinations_checked,
            'valid_combinations_count': valid_combinations_count,
            'never_occurred_count': len(all_never_occurred),
            'occurred_count': len(all_occurred),
            'min_occurrence': min([x['occurrence_count'] for x in all_occurred]) if all_occurred else 0,
            'max_occurrence': max([x['occurrence_count'] for x in all_occurred]) if all_occurred else 0,
            'avg_occurrence': sum([x['occurrence_count'] for x in all_occurred]) / len(
                all_occurred) if all_occurred else 0
        }

        self.logger.info(f"Analysis complete: {stats}")

        return {
            'never_occurred': all_never_occurred[:self.config.MAX_RESULTS_PER_CATEGORY],
            'least_occurred': all_occurred_sorted[:self.config.MAX_RESULTS_PER_CATEGORY],
            'most_occurred': list(reversed(all_occurred_sorted[-self.config.MAX_RESULTS_PER_CATEGORY:])),
            'stats': stats
        }