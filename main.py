import logging
import time
from datetime import timedelta
from datetime import datetime
from typing import List, Dict, Any
import json

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

        # REMOVED: Old cache initialization - using unified cache in APIFootballClient

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
        for league_name, league_id in league_items[:2]:  # Limit to 2 leagues for testing
            for season in self.config.analysis.SEASON[:1]:  # Limit to 1 season for testing
                self.logger.info(f"📊 Fetching matches for {league_name} ({season})...")

                # STEP 1: Get fixtures list for this league+season
                fixtures_response = self.api_client.get_matches(
                    league_id=league_id,
                    season=season
                )

                if not fixtures_response:
                    self.logger.warning(f"No fixtures returned for {league_name}, season {season}")
                    continue

                self.logger.info(f"📥 Found {len(fixtures_response)} fixtures for {league_name}")

                league_matches = []
                processed_count = 0

                # STEP 2: Process each fixture into detailed Match objects
                for fixture_data in fixtures_response[:2]:  # Limit to 5 matches for testing
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
                    f"🎯 Successfully processed {processed_count} matches for {league_name}")
                matches.extend(league_matches)

        self.logger.info(f"📈 Total matches fetched for analysis: {len(matches)}")
        return matches

    def _print_results(self, results: Dict[str, Any]):
        print("\n" + "=" * 80)
        print("FOOTBALL EVENT PATTERN ANALYSIS RESULTS")
        print("=" * 80)

        for league, league_data in results.items():
            print(f"\n### {league.upper()} ###")
            print(f"Matches analyzed: {league_data['total_matches']}")
            print(f"Patterns analyzed: {league_data['total_patterns_analyzed']}")
            print(f"Combination strategy: {league_data['combination_strategy']}")

            # Print statistics if available
            if 'stats' in league_data:
                stats = league_data['stats']
                print(f"\n📊 ANALYSIS STATISTICS:")
                print(f"   Total combinations checked: {stats['total_combinations_checked']:,}")
                print(f"   Valid combinations: {stats['valid_combinations_count']:,}")
                print(f"   Never occurred: {stats['never_occurred_count']:,}")
                print(f"   Occurred at least once: {stats['occurred_count']:,}")
                if stats['occurred_count'] > 0:
                    print(f"   Occurrence range: {stats['min_occurrence']} - {stats['max_occurrence']}")
                    print(f"   Average occurrence: {stats['avg_occurrence']:.2f}")

            # Never Occurred Combinations
            print("\n" + "🔍 " + "-" * 38)
            print("NEVER OCCURRED COMBINATIONS")
            print("-" * 40)

            never_occurred = league_data['never_occurred']
            if never_occurred:
                for i, combo in enumerate(never_occurred[:5], 1):
                    print(f"\n{i}. Combination of {combo['combination_size']} events:")
                    for event in combo['events']:
                        event_type = event.get('event_type', 'Unknown')
                        market = event.get('market', 'Unknown')
                        print(f"   📍 {event['description']}")
                        print(f"     Type: {event_type}, Market: {market}")
                    print(f"   ❌ Occurrences: {combo['occurrence_count']} ({combo['percentage']:.4f}%)")
            else:
                print("   No never-occurred combinations found.")

            # Least Occurred Combinations (occurred at least once)
            print("\n" + "📉 " + "-" * 38)
            print("LEAST OCCURRED COMBINATIONS")
            print("-" * 40)

            least_occurred = league_data['least_occurred']
            if least_occurred:
                for i, combo in enumerate(least_occurred[:5], 1):
                    print(f"\n{i}. Combination of {combo['combination_size']} events:")
                    for event in combo['events']:
                        event_type = event.get('event_type', 'Unknown')
                        market = event.get('market', 'Unknown')
                        print(f"   📍 {event['description']}")
                        print(f"     Type: {event_type}, Market: {market}")
                    print(f"   📊 Occurrences: {combo['occurrence_count']} ({combo['percentage']:.4f}%)")
            else:
                print("   No least-occurred combinations found.")

            # Most Occurred Combinations
            print("\n" + "📈 " + "-" * 38)
            print("MOST OCCURRED COMBINATIONS")
            print("-" * 40)

            most_occurred = league_data['most_occurred']
            if most_occurred:
                for i, combo in enumerate(most_occurred[:5], 1):
                    print(f"\n{i}. Combination of {combo['combination_size']} events:")
                    for event in combo['events']:
                        event_type = event.get('event_type', 'Unknown')
                        market = event.get('market', 'Unknown')
                        print(f"   📍 {event['description']}")
                        print(f"     Type: {event_type}, Market: {market}")
                    print(f"   🎯 Occurrences: {combo['occurrence_count']} ({combo['percentage']:.4f}%)")
            else:
                print("   No most-occurred combinations found.")

            # Summary
            print("\n" + "📋 " + "-" * 38)
            print("SUMMARY")
            print("-" * 40)
            print(f"Never occurred: {len(never_occurred)} combinations")
            print(f"Least occurred: {len(least_occurred)} combinations")
            print(f"Most occurred: {len(most_occurred)} combinations")

            # Calculate some insights
            total_combinations = len(never_occurred) + len(least_occurred) + len(most_occurred)
            if total_combinations > 0:
                never_percentage = (len(never_occurred) / total_combinations) * 100
                print(f"Never occurred ratio: {never_percentage:.1f}%")

            # Find the most interesting patterns (very rare but occurred)
            if least_occurred:
                rarest = least_occurred[0]
                print(f"\n🎲 Rarest occurred pattern: {rarest['occurrence_count']} occurrence(s)")

            if most_occurred:
                most_common = most_occurred[0]
                print(f"🏆 Most common pattern: {most_common['occurrence_count']} occurrence(s)")

            print("\n" + "=" * 80)


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