import logging
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

    def run_analysis(self) -> Dict[str, Any]:
        """Main analysis workflow"""
        self.logger.info("Starting football data analysis")

        # In a real implementation, this would fetch actual data from API
        # For demonstration, we'll use sample data
        sample_matches = self._get_sample_matches()

        # Analyze patterns
        results = self.pattern_analyzer.analyze_matches(sample_matches)

        # Save results
        timestamp = "2024_results"  # In real implementation, use actual timestamp
        save_results(results, f"football_analysis_{timestamp}.json")

        self._print_results(results)
        return results

    def _get_sample_matches(self) -> List[Match]:
        """Fetch recent football matches from the API for analysis"""
        self.logger.info("Fetching sample football matches from API...")

        matches: List[Match] = []
        leagues_response = self.api_client.get_leagues()

        if not leagues_response or "response" not in leagues_response:
            self.logger.error("Failed to retrieve leagues data from API")
            return []

        league_name_to_id = {}
        for league_info in leagues_response["response"]:
            name = league_info["league"]["name"]
            if name in self.config.analysis.LEAGUES:
                league_name_to_id[name] = league_info["league"]["id"]

        if not league_name_to_id:
            self.logger.warning("No configured leagues found in API response.")
            return []

        # Limit sample to avoid API quota exhaustion
        for league_name, league_id in list(league_name_to_id.items())[:1]:
            self.logger.info(f"Fetching matches for league: {league_name}")
            fixtures_response = self.api_client.get_matches(
                league_id=league_id,
                season=self.config.analysis.SEASON
            )

            if not fixtures_response or "response" not in fixtures_response:
                self.logger.warning(f"No fixtures returned for league {league_name}")
                continue

            # Take up to 10 matches per league for sampling
            for fixture_data in fixtures_response["response"][:1]:
                print(f"Match fixture_data:\n {fixture_data}")
                try:
                    match = self.api_client.parse_match_data(fixture_data)
                    print(f"Match:\n {match}")
                    matches.append(match)
                except Exception as e:
                    self.logger.error(f"Failed to parse match data: {e}")

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
