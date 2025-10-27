import logging
import time
from datetime import timedelta
from datetime import datetime
from typing import List, Dict, Any
import json

from config.settings import Config, AnalysisConfig
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

    def run_analysis(self) -> Dict[str, Any]:
        """Main analysis workflow"""
        self.logger.info("Starting football data analysis")

        sample_matches = self._get_sample_matches()

        # Debug cache state
        # self._debug_cache_state()

        # Analyze patterns
        results = self.pattern_analyzer.analyze_matches(sample_matches)

        print("Saving result to file")

        # Ensure results folder exists
        import os
        results_dir = "results"
        os.makedirs(results_dir, exist_ok=True)

        # Save to results folder
        filepath = os.path.join(results_dir, "football_analysis.json")
        save_results(results, filepath)

        self._print_results()
        return results

    def _debug_cache_state(self):
        """Debug method to check cache state"""
        cache_stats = self.api_client.cache.get_cache_stats()
        self.logger.info(f"🔍 CACHE DEBUG: {cache_stats}")

        # Check each league in cache
        for league_id, league_data in self.api_client.cache.cache_data.get('leagues', {}).items():
            for season, season_data in league_data.get('seasons', {}).items():
                match_count = len(season_data.get('matches', {}))
                self.logger.info(f"🔍 League {league_id}, Season {season}: {match_count} matches")
                for match_id, match_data in season_data.get('matches', {}).items():
                    has_details = match_data.get('has_details', False)
                    self.logger.info(f"🔍   Match {match_id}: has_details={has_details}")

    def _get_sample_matches(self) -> List[Match]:
        """Fetch football matches from the API for analysis with multiple seasons"""
        self.logger.info("Fetching football matches from API...")

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

        # Convert dict_items to list for slicing
        league_items = list(league_name_to_id.items())

        # Process each league and season
        number_of_leagues = len(league_items)
        seasons_per_leagues = 1  # len(self.config.analysis.SEASON)
        matches_per_season = 0
        for league_name, league_id in league_items[:number_of_leagues]:
            if league_name.lower() != "Serie A".lower():
                continue

            # Limit to 2 leagues for testing
            for season in self.config.analysis.SEASON[:seasons_per_leagues]:  # Limit to 1 season for testing
                self.logger.info(f"📊 Fetching matches for {league_name} ({season})...")

                # STEP 1: Get fixtures list for this league+season
                fixtures_response = self.api_client.get_matches(
                    league_id=league_id,
                    season=season
                )

                matches_per_season = len(fixtures_response)

                if not fixtures_response:
                    self.logger.warning(f"No fixtures returned for {league_name}, season {season}")
                    continue

                self.logger.info(f"📥 Found {len(fixtures_response)} fixtures for {league_name}")

                league_matches = []
                processed_count = 0

                # STEP 2: Process each fixture into detailed Match objects
                for fixture_data in fixtures_response[:matches_per_season]:  # Use the defined variable
                    try:
                        self.logger.info(f"🔄 Processing match {fixture_data['fixture']['id']}: "
                                         f"{fixture_data['teams']['home']['name']} vs "
                                         f"{fixture_data['teams']['away']['name']}")

                        match = self.api_client.parse_match_data(fixture_data)
                        league_matches.append(match)
                        processed_count += 1

                        self.logger.info(f"✅ Processed match {match.id}: {match.home_team} vs {match.away_team}")

                    except Exception as e:
                        self.logger.error(f"❌ Failed to parse match data: {e}")
                        continue

                self.logger.info(
                    f"🎯 Successfully processed {processed_count}/{seasons_per_leagues * matches_per_season} matches "
                    f"for {league_name}")
                matches.extend(league_matches)

        # Debug: Check why we might be missing matches
        expected_matches = number_of_leagues * seasons_per_leagues * matches_per_season  # 2 leagues × 2 matches each
        # = 4 matches
        if len(matches) < expected_matches:
            self.logger.warning(
                f"⚠️  Expected {expected_matches} matches but got {len(matches)}. Some matches failed to process.")

        self.logger.info(f"📈 Total matches fetched for analysis: {len(matches)}")
        return matches

    def _print_results(self):
        """Print comprehensive results for each league and season separately"""
        print("\n" + "=" * 100)
        print("🎯 COMPREHENSIVE FOOTBALL EVENT PATTERN ANALYSIS RESULTS")
        print("=" * 100)

        value_mode = self.pattern_analyzer.use_odd_info  # 👈 detect whether odds mode is active
        all_results = self.pattern_analyzer.results_manager.get_all_results()

        for league_id, league_data in all_results['leagues'].items():
            league_name = league_data['name']
            print(f"\n🏆 LEAGUE: {league_name.upper()} (ID: {league_id})")
            print("-" * 80)

            for season, season_data in league_data['seasons'].items():
                print(f"\n📅 SEASON: {season}")
                print(f"📊 Matches analyzed: {season_data['total_matches_processed']}")
                print(f"🔢 Combinations analyzed: {len(season_data['combos'])}")

                analysis = season_data.get('analysis_results', {})
                if not analysis:
                    print("⚠️  No analysis results found.")
                    continue

                # ---------------------------------------------------------------------
                # 💰 VALUE-BET MODE
                # ---------------------------------------------------------------------
                if value_mode:
                    print("\n💰 VALUE BET MODE ACTIVE")
                    print("───────────────────────────────────────────────────────────────")

                    most_valuable = analysis.get('most_valuable', [])
                    least_valuable = analysis.get('least_valuable', [])
                    stats = analysis.get('stats', {})

                    print(f"\n📈 Total positive value bets found: {stats.get('total_value_bets', 0)}")
                    print(f"   Highest value: {stats.get('highest_value', 0):.2f}%")
                    print(f"   Lowest positive value: {stats.get('lowest_value', 0):.2f}%")

                    # --- Most valuable ---
                    print(f"\n💎 TOP {len(most_valuable)} MOST VALUABLE BETS:")
                    print("───────────────────────────────────────────────────────────────")
                    for i, combo in enumerate(most_valuable[:AnalysisConfig.MAX_RESULTS_PER_CATEGORY], 1):
                        odds_info = combo.get('odds_info') or {}
                        value = odds_info.get('value_indicator', 0)
                        odds = odds_info.get('combined_odds', 0)
                        occ = combo.get('occurrence_count', 0)
                        pct = combo.get('percentage', 0)

                        print(f"\n{i}. 💰 Value: +{value:.2f}% | Odds: {odds:.2f} | Occurred {occ}× ({pct:.2f}%)")
                        for event in combo['events'][:3]:
                            print(f"   📍 {event['description']} ({event['event_type']}, {event['market']})")

                    # --- Least valuable ---
                    print(f"\n📉 LOWEST POSITIVE VALUE BETS:")
                    print("───────────────────────────────────────────────────────────────")
                    for i, combo in enumerate(least_valuable[:10], 1):
                        odds_info = combo.get('odds_info') or {}
                        value = odds_info.get('value_indicator', 0)
                        odds = odds_info.get('combined_odds', 0)
                        occ = combo.get('occurrence_count', 0)
                        pct = combo.get('percentage', 0)

                        print(f"\n{i}. 💵 Value: +{value:.2f}% | Odds: {odds:.2f} | Occurred {occ}× ({pct:.2f}%)")
                        for event in combo['events'][:3]:
                            print(f"   📍 {event['description']} ({event['event_type']}, {event['market']})")

                # ---------------------------------------------------------------------
                # 📊 NORMAL (PATTERN OCCURRENCE) MODE
                # ---------------------------------------------------------------------
                else:
                    print("\n📈 ANALYSIS STATISTICS:")
                    stats = analysis.get('stats', {})
                    print(f"   Total combinations checked: {stats.get('total_combinations_checked', 0):,}")
                    print(f"   Valid combinations: {stats.get('valid_combinations_count', 0):,}")
                    print(f"   Never occurred: {stats.get('never_occurred_count', 0):,}")
                    print(f"   Occurred at least once: {stats.get('occurred_count', 0):,}")

                    if stats.get('occurred_count', 0) > 0:
                        print(
                            f"   Occurrence range: {stats.get('min_occurrence', 0)} - {stats.get('max_occurrence', 0)}")
                        print(f"   Average occurrence: {stats.get('avg_occurrence', 0):.2f}")

                    # Loop through combination sizes
                    organized_results = analysis.get('organized_results', {})
                    for combo_size in sorted(organized_results.keys()):
                        size_results = organized_results[combo_size]
                        print(f"\n{'=' * 80}")
                        print(f"🔢 COMBINATION SIZE: {combo_size} EVENTS")
                        print(f"{'=' * 80}")

                        most_occurred = size_results.get('most_occurred', [])
                        least_occurred = size_results.get('least_occurred', [])

                        # --- Most occurred ---
                        if most_occurred:
                            print(f"\n📈 MOST OCCURRED COMBINATIONS:")
                            for i, combo in enumerate(most_occurred[:AnalysisConfig.MAX_RESULTS_PER_CATEGORY], 1):
                                print(f"\n{i}. {combo['occurrence_count']} occurrences ({combo['percentage']:.2f}%)")
                                for event in combo['events']:
                                    print(f"   📍 {event['description']} ({event['event_type']}, {event['market']})")

                        # --- Least occurred ---
                        if least_occurred:
                            print(f"\n📉 LEAST OCCURRED COMBINATIONS:")
                            for i, combo in enumerate(least_occurred[:3], 1):
                                print(f"\n{i}. {combo['occurrence_count']} occurrences ({combo['percentage']:.2f}%)")
                                for event in combo['events']:
                                    print(f"   📍 {event['description']} ({event['event_type']}, {event['market']})")

        print("\n💾 Results saved to: comprehensive_results.json")
        print("=" * 100)


def main():
    """Main entry point"""
    start_time = time.time()
    config = Config()
    analyzer = FootballDataAnalyzer(config)

    try:
        results = analyzer.run_analysis()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n✅ Analysis completed successfully!")
        print(f"⏱️  Execution time: {execution_time:.2f} seconds ({timedelta(seconds=int(execution_time))})")
    except Exception as e:
        logging.error(f"Analysis failed: {e}")
        raise


if __name__ == "__main__":
    main()
