import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import json
import os

from config.settings import Config
from clients.football_api import APIFootballClient
from analyzers.pattern_analyzer import PatternAnalyzer
from data.models import Match
from utils.logger import setup_logger
from utils.helpers import save_results


class FootballDataAnalyzer:
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger(__name__)
        self.api_client = APIFootballClient(config.api)
        self.pattern_analyzer = PatternAnalyzer(config.analysis)

        # Initialize match cache
        self.match_cache_dir = "match_cache"
        self._ensure_match_cache_dir()

    def _ensure_match_cache_dir(self):
        """Create match cache directory if it doesn't exist"""
        if not os.path.exists(self.match_cache_dir):
            os.makedirs(self.match_cache_dir)

    def _get_match_cache_file(self, league_id: int, season: int) -> str:
        """Get cache file path for league and season"""
        return os.path.join(self.match_cache_dir, f"matches_{league_id}_{season}.json")

    def _load_cached_matches(self, league_id: int, season: int) -> Optional[List[Match]]:
        """Load matches from cache"""
        cache_file = self._get_match_cache_file(league_id, season)

        if not os.path.exists(cache_file):
            return None

        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cached_data = json.load(f)

            # Check if cache is expired (1 day TTL for match data)
            cache_time = datetime.fromisoformat(cached_data['timestamp'])
            current_time = datetime.now()
            time_diff = (current_time - cache_time).total_seconds()

            if time_diff > 86400:  # 24 hours
                self.logger.debug(f"Match cache expired for league {league_id}, season {season}")
                return None

            matches = []
            for match_data in cached_data['matches']:
                # Reconstruct Match objects from cached data
                match = Match(**match_data)
                matches.append(match)

            self.logger.info(f"Loaded {len(matches)} matches from cache for league {league_id}")
            return matches

        except (json.JSONDecodeError, KeyError, ValueError, TypeError) as e:
            self.logger.warning(f"Invalid match cache file {cache_file}: {e}")
            try:
                os.remove(cache_file)
            except OSError:
                pass
            return None

    def _save_matches_to_cache(self, league_id: int, season: int, matches: List[Match]):
        """Save matches to cache"""
        cache_file = self._get_match_cache_file(league_id, season)

        try:
            cache_data = {
                'timestamp': datetime.now().isoformat(),
                'league_id': league_id,
                'season': season,
                'matches': [match.to_dict() for match in matches]
            }

            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, ensure_ascii=False, default=str)

            self.logger.debug(f"Cached {len(matches)} matches for league {league_id}, season {season}")

        except Exception as e:
            self.logger.error(f"Failed to cache matches: {e}")

    def run_analysis(self) -> Dict[str, Any]:
        """Main analysis workflow"""
        self.logger.info("Starting football data analysis")

        sample_matches = self._get_sample_matches()

        # Analyze patterns
        results = self.pattern_analyzer.analyze_matches(sample_matches)

        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_results(results, f"football_analysis_{timestamp}.json")

        self._print_results(results)
        return results

    def _get_sample_matches(self) -> List[Match]:
        """Fetch recent football matches from the API for analysis"""
        self.logger.info("Fetching sample football matches from API...")

        matches: List[Match] = []
        leagues_response = self.api_client.get_leagues()

        if not leagues_response:
            self.logger.error("Failed to retrieve leagues data from API")
            return []

        league_name_to_id = {}
        for league_info in leagues_response:
            name = league_info["league"]["name"]
            if name in self.config.analysis.LEAGUES:
                league_name_to_id[name] = league_info["league"]["id"]

        if not league_name_to_id:
            self.logger.warning("No configured leagues found in API response.")
            return []

        # Limit sample to avoid API quota exhaustion
        for league_name, league_id in list(league_name_to_id.items())[:1]:
            self.logger.info(f"Fetching matches for league: {league_name}")

            # Try to load from cache first
            cached_matches = self._load_cached_matches(league_id, self.config.analysis.SEASON)
            if cached_matches:
                matches.extend(cached_matches)
                continue

            # If not in cache, fetch from API
            fixtures_response = self.api_client.get_matches(
                league_id=league_id,
                season=self.config.analysis.SEASON
            )

            if not fixtures_response:
                self.logger.warning(f"No fixtures returned for league {league_name}")
                continue

            league_matches = []
            # Take up to 10 matches per league for sampling
            for fixture_data in fixtures_response[:10]:
                try:
                    match = self.api_client.parse_match_data(fixture_data)
                    league_matches.append(match)
                except Exception as e:
                    self.logger.error(f"Failed to parse match data: {e}")

            # Cache the fetched matches
            if league_matches:
                self._save_matches_to_cache(league_id, self.config.analysis.SEASON, league_matches)
                matches.extend(league_matches)

        self.logger.info(f"Fetched {len(matches)} matches for analysis.")
        return matches

    def _print_results(self, results: Dict[str, Any]):
        print("\n" + "=" * 80)
        print("FOOTBALL EVENT PATTERN ANALYSIS RESULTS")
        print("=" * 80)

        for league, league_data in results.items():
            print(f"\n### {league.upper()} ###")
            print(f"Matches analyzed: {league_data['total_matches']}")
            print(f"Patterns analyzed: {league_data['total_patterns_analyzed']}")

            for category in ['never_occurred', 'least_occurred', 'most_occurred']:
                print("\n" + "-" * 40)
                print(f"{category.replace('_', ' ').upper()} (Top 5)")
                print("-" * 40)

                for i, combo in enumerate(league_data[category][:5], 1):
                    print(f"\n{i}. Combination of {combo['combination_size']} events:")
                    for event in combo['events']:
                        print(f"   - {event['description']}")
                    print(f"   Occurrences: {combo['occurrence_count']} ({combo['percentage']:.4f}%)")


def main():
    """Main entry point"""
    config = Config()
    analyzer = FootballDataAnalyzer(config)

    try:
        results = analyzer.run_analysis()
        print("\nAnalysis completed successfully!")
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        raise


if __name__ == "__main__":
    main()