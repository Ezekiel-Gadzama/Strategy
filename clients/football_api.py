import requests
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from config.settings import APIConfig
from data.models import Match, MatchEvent, EventType, TeamStats, HalfStats
from utils.cache_manager import OrganizedCacheManager


class APIFootballClient:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'x-rapidapi-key': config.API_KEY,
            'x-rapidapi-host': 'v3.football.api-sports.io'
        })
        self.logger = logging.getLogger(__name__)
        self.last_request_time = 0
        # Use organized cache manager
        self.cache = OrganizedCacheManager(cache_dir="api_cache", ttl=config.CACHE_TTL)

    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 60 / self.config.RATE_LIMIT

        if time_since_last < min_interval:
            time.sleep(min_interval - time_since_last)
        self.last_request_time = time.time()

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make API request with error handling"""
        self._rate_limit()

        try:
            url = f"{self.config.BASE_URL}/{endpoint}"
            response = self.session.get(url, params=params, timeout=self.config.TIMEOUT)
            response.raise_for_status()
            api_response = response.json()
            return api_response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed for {endpoint}: {e}")
            return None

    def get_leagues(self) -> List[Dict[str, Any]]:
        """Get available leagues"""
        response = self._make_request("leagues", {"current": "true"})
        if response:
            # Save league info to organized cache
            for league_info in response.get("response", []):
                league_id = league_info["league"]["id"]
                self.cache.save_league_info(league_id, league_info)
        return response.get("response", []) if response else []

    def get_matches(self, league_id: int, season: int, round: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get matches for a league and season"""
        params = {'league': league_id, 'season': season}
        if round:
            params['round'] = round

        # Check if we have cached matches
        cached_matches = self.cache.get_league_matches(league_id, season)
        if cached_matches:
            self.logger.info(f"Using cached matches for league {league_id}, season {season}")
            return [match_data['fixture_data'] for match_data in cached_matches.values()]

        # If not in cache, make API request
        response = self._make_request("fixtures", params)
        if response:
            matches_data = response.get("response", [])
            # Save matches to organized cache
            self.cache.save_matches(league_id, season, matches_data)
            return matches_data
        return []

    def get_match_events(self, match_id: int, league_id: int, season: int) -> List[Dict[str, Any]]:
        """Get events for a specific match - check cache first"""
        # Check if we have processed match data in organized cache
        match_details = self.cache.get_match_details(league_id, season, match_id)
        if match_details and 'events' in match_details:
            return match_details['events']

        # If not in cache, make API request
        params = {'fixture': match_id}
        response = self._make_request("fixtures/events", params)
        events_data = response.get("response", []) if response else []

        # Save events to organized cache
        if events_data:
            # Get existing statistics or empty list
            existing_stats = []
            if match_details and 'statistics' in match_details:
                existing_stats = match_details['statistics']

            self.cache.save_match_details(league_id, season, match_id, events_data, existing_stats)

        return events_data

    def get_match_statistics(self, match_id: int, league_id: int, season: int) -> List[Dict[str, Any]]:
        """Get statistics for a specific match - check cache first"""
        # Check if we have processed match data in organized cache
        match_details = self.cache.get_match_details(league_id, season, match_id)
        if match_details and 'statistics' in match_details:
            return match_details['statistics']

        # If not in cache, make API request
        params = {'fixture': match_id}
        response = self._make_request("fixtures/statistics", params)
        stats_data = response.get("response", []) if response else []

        # Save statistics to organized cache
        if stats_data:
            # Get existing events or empty list
            existing_events = []
            if match_details and 'events' in match_details:
                existing_events = match_details['events']

            self.cache.save_match_details(league_id, season, match_id, existing_events, stats_data)

        return stats_data

    def get_match_lineups(self, match_id: int) -> List[Dict[str, Any]]:
        """Get lineups for a specific match"""
        params = {'fixture': match_id}
        response = self._make_request("fixtures/lineups", params)
        return response.get("response", []) if response else []

    def parse_match_data(self, match_data: Dict[str, Any]) -> Match:
        """Parse raw match data into comprehensive Match object"""
        fixture = match_data['fixture']
        league = match_data['league']
        teams = match_data['teams']
        goals = match_data['goals']
        score = match_data.get('score', {})

        # Create basic match object
        match = Match(
            id=fixture['id'],
            league=league['name'],
            league_id=league['id'],
            season=league['season'],
            date=fixture['date'],
            home_team=teams['home']['name'],
            home_team_id=teams['home']['id'],
            away_team=teams['away']['name'],
            away_team_id=teams['away']['id'],
            score_home=goals['home'] or 0,
            score_away=goals['away'] or 0,
            status=fixture['status']['short'],
            referee=fixture.get('referee'),
            venue_id=match_data.get('venue', {}).get('id'),
            venue_city=match_data.get('venue', {}).get('city')
        )

        # Fetch and process additional data
        self._enrich_match_data(match)
        return match

    def _enrich_match_data(self, match: Match):
        """Enrich match data with events, statistics, and detailed info"""
        # Check if we have complete cached match data in organized cache
        match_details = self.cache.get_match_details(match.league_id, match.season, match.id)
        if match_details and match_details.get('has_details'):  # Changed from 'processed' to 'has_details'
            # Load from organized cache
            self.logger.info(f"📦 Loading match {match.id} from cache")
            self._load_match_from_organized_cache(match, match_details)
            return

        self.logger.info(f"🔄 Fetching details for match {match.id} from API")

        # Get match events using organized cache
        events_data = self.get_match_events(match.id, match.league_id, match.season)
        self._process_events(match, events_data)

        # Get match statistics using organized cache
        stats_data = self.get_match_statistics(match.id, match.league_id, match.season)
        self._process_statistics(match, stats_data)

        # Extract half-time statistics from events
        self._extract_half_stats(match, events_data)

        # Generate derived events for pattern analysis
        self._generate_derived_events(match)

    def _load_match_from_organized_cache(self, match: Match, match_details: Dict[str, Any]):
        """Load match data from organized cache"""
        match.events = []
        for event_dict in match_details.get('events', []):
            try:
                # Filter out parameters that MatchEvent doesn't accept
                valid_params = ['event_type', 'type', 'value', 'team', 'minute', 'is_home', 'description']
                filtered_event_dict = {k: v for k, v in event_dict.items() if k in valid_params}

                # Handle both 'type' and 'event_type' parameter names
                if 'type' in filtered_event_dict and 'event_type' not in filtered_event_dict:
                    filtered_event_dict = filtered_event_dict.copy()
                    filtered_event_dict['event_type'] = filtered_event_dict.pop('type')

                # Convert string event_type back to EventType enum
                if isinstance(filtered_event_dict.get('event_type'), str):
                    # Map API event types to EventType enum values
                    event_type_str = filtered_event_dict['event_type'].lower()
                    event_type_mapping = {
                        'goal': EventType.GOALS,
                        'card': EventType.CARDS,
                        'yellow card': EventType.CARDS,
                        'red card': EventType.CARDS,
                        'corner': EventType.CORNERS,
                        'subst': EventType.TEAM_STATS,
                        'var': EventType.TEAM_STATS,
                        'foul': EventType.FOULS,
                        'offside': EventType.OFFSIDES,
                        'half_stats': EventType.HALF_STATS,
                        'goals': EventType.GOALS,
                        'cards': EventType.CARDS,
                        'corners': EventType.CORNERS,
                        'team_stats': EventType.TEAM_STATS,
                        'fouls': EventType.FOULS,
                        'offsides': EventType.OFFSIDES
                    }

                    if event_type_str in event_type_mapping:
                        filtered_event_dict['event_type'] = event_type_mapping[event_type_str]
                    else:
                        # Default to TEAM_STATS for unknown event types
                        filtered_event_dict['event_type'] = EventType.TEAM_STATS
                        self.logger.warning(
                            f"Unknown event type '{filtered_event_dict['event_type']}', defaulting to TEAM_STATS")

                # Extract minute from 'time' field if it exists in original data
                if 'minute' not in filtered_event_dict and 'time' in event_dict:
                    time_data = event_dict.get('time', {})
                    if 'elapsed' in time_data:
                        filtered_event_dict['minute'] = time_data['elapsed']

                # Ensure required 'value' parameter exists (default to 1 if missing)
                if 'value' not in filtered_event_dict:
                    filtered_event_dict['value'] = 1  # Default value for events

                # Ensure required parameters exist
                required_params = ['event_type', 'value']
                for param in required_params:
                    if param not in filtered_event_dict:
                        self.logger.warning(f"Missing required parameter '{param}' in event, using default")
                        if param == 'value':
                            filtered_event_dict[param] = 1
                        elif param == 'event_type':
                            filtered_event_dict[param] = EventType.TEAM_STATS

                event = MatchEvent(**filtered_event_dict)
                match.events.append(event)
            except Exception as e:
                self.logger.warning(f"Failed to load event from cache: {e}")
                continue

        # Process statistics from cache
        stats_data = match_details.get('statistics', [])
        self._process_statistics(match, stats_data)

        # Extract half stats from events
        self._extract_half_stats(match, match_details.get('events', []))

        # Generate derived events
        self._generate_derived_events(match)

    def _cache_complete_match(self, match: Match):
        """Cache complete match data for future use"""
        match_data = {
            'complete': True,
            'events': [event.to_dict() for event in match.events],
            'home_stats': match.home_stats.__dict__ if match.home_stats else None,
            'away_stats': match.away_stats.__dict__ if match.away_stats else None,
            'first_half': match.first_half.__dict__,
            'second_half': match.second_half.__dict__,
            'basic_info': {
                'league': match.league,
                'season': match.season,
                'home_team': match.home_team,
                'away_team': match.away_team,
                'score_home': match.score_home,
                'score_away': match.score_away
            }
        }
        self.cache.set_match_data(match.id, match_data)

    def _process_events(self, match: Match, events_data: List[Dict[str, Any]]):
        """Process match events"""
        for event_data in events_data:
            event_type = self._classify_event_type(event_data)
            if not event_type:
                continue

            event = MatchEvent(
                event_type=event_type,
                value=1,  # Count for discrete events
                team=event_data.get('team', {}).get('name'),
                minute=event_data.get('time', {}).get('elapsed'),
                is_home=event_data.get('team', {}).get('id') == match.home_team_id,
                description=self._get_event_description(event_data)
            )
            match.events.append(event)

    def _classify_event_type(self, event_data: Dict[str, Any]) -> Optional[EventType]:
        """Classify event type from API data"""
        event_type = event_data.get('type')
        detail = event_data.get('detail')

        event_type_mapping = {
            'goal': EventType.GOALS,
            'penalty': EventType.GOALS,
            'missed penalty': EventType.GOALS,
            'card': EventType.CARDS,
            'yellow card': EventType.CARDS,
            'red card': EventType.CARDS,
            'corner': EventType.CORNERS,
            'subst': EventType.TEAM_STATS,
            'var': EventType.TEAM_STATS,
            'foul': EventType.FOULS,
            'offside': EventType.OFFSIDES
        }

        if event_type and event_type.lower() in event_type_mapping:
            return event_type_mapping[event_type.lower()]

        return None

    def _get_event_description(self, event_data: Dict[str, Any]) -> str:
        """Generate descriptive text for event"""
        event_type = event_data.get('type', '')
        detail = event_data.get('detail', '')
        player = event_data.get('player', {}).get('name', '')

        if event_type == 'Goal':
            if detail == 'Normal Goal':
                return f"Goal by {player}"
            elif detail == 'Own Goal':
                return f"Own goal by {player}"
            elif detail == 'Penalty':
                return f"Penalty goal by {player}"
        elif event_type in ['Yellow Card', 'Red Card']:
            return f"{event_type} for {player}"
        elif event_type == 'Corner':
            return "Corner kick"

        return f"{event_type}: {detail}"

    def _process_statistics(self, match: Match, stats_data: List[Dict[str, Any]]):
        """Process match statistics"""
        if not stats_data:
            return

        for team_stats in stats_data:
            team_id = team_stats['team']['id']
            is_home = team_id == match.home_team_id

            stats_dict = {}
            for stat in team_stats.get('statistics', []):
                stats_dict[stat['type']] = self._safe_convert_stat(stat['value'])

            team_stats_obj = TeamStats(
                team_id=team_id,
                team_name=team_stats['team']['name'],
                shots_on_goal=stats_dict.get('Shots on Goal', 0),
                shots_off_goal=stats_dict.get('Shots off Goal', 0),
                shots_insidebox=stats_dict.get('Shots insidebox', 0),
                shots_outsidebox=stats_dict.get('Shots outsidebox', 0),
                total_shots=stats_dict.get('Total Shots', 0),
                blocked_shots=stats_dict.get('Blocked Shots', 0),
                fouls=stats_dict.get('Fouls', 0),
                corner_kicks=stats_dict.get('Corner Kicks', 0),
                offsides=stats_dict.get('Offsides', 0),
                ball_possession=stats_dict.get('Ball Possession', 0),
                yellow_cards=stats_dict.get('Yellow Cards', 0),
                red_cards=stats_dict.get('Red Cards', 0),
                goalkeeper_saves=stats_dict.get('Goalkeeper Saves', 0),
                total_passes=stats_dict.get('Total passes', 0),
                passes_accurate=stats_dict.get('Passes accurate', 0),
                passes_percentage=stats_dict.get('Passes %', 0.0)
            )

            if is_home:
                match.home_stats = team_stats_obj
            else:
                match.away_stats = team_stats_obj

    def _extract_half_stats(self, match: Match, events_data: List[Dict[str, Any]]):
        """Extract statistics for each half from events"""
        first_half = HalfStats()
        second_half = HalfStats()

        for event in events_data:
            minute = event.get('time', {}).get('elapsed')
            if not minute:
                continue

            is_home = event.get('team', {}).get('id') == match.home_team_id
            half = first_half if minute <= 45 else second_half

            # Count goals
            if event.get('type') == 'Goal':
                if is_home:
                    half.home_goals += 1
                else:
                    half.away_goals += 1

            # Count cards
            elif event.get('type') in ['Yellow Card', 'Red Card']:
                if is_home:
                    half.home_cards += 1
                else:
                    half.away_cards += 1

            # Count corners
            elif event.get('type') == 'Corner':
                if is_home:
                    half.home_corners += 1
                else:
                    half.away_corners += 1

        match.first_half = first_half
        match.second_half = second_half

    def _generate_derived_events(self, match: Match):
        """Generate derived events for pattern analysis"""
        # Half-time result events
        first_half_result = self._get_half_result(match.first_half)
        match.events.append(MatchEvent(
            event_type=EventType.HALF_STATS,
            value=first_half_result,
            description="first_half_result"
        ))

        # Total cards
        total_cards = ((match.home_stats.yellow_cards + match.home_stats.red_cards) if match.home_stats else 0) + \
                      ((match.away_stats.yellow_cards + match.away_stats.red_cards) if match.away_stats else 0)
        match.events.append(MatchEvent(
            event_type=EventType.CARDS,
            value=total_cards,
            description="total_cards"
        ))

        # Total corners
        total_corners = ((match.home_stats.corner_kicks if match.home_stats else 0) +
                         (match.away_stats.corner_kicks if match.away_stats else 0))
        match.events.append(MatchEvent(
            event_type=EventType.CORNERS,
            value=total_corners,
            description="total_corners"
        ))

        # Add more derived events as needed...

    def _get_half_result(self, half: HalfStats) -> str:
        """Get result for a half"""
        if half.home_goals > half.away_goals:
            return "home"
        elif half.away_goals > half.home_goals:
            return "away"
        else:
            return "draw"

    def _safe_convert_stat(self, value: Any) -> Any:
        """Safely convert statistic values"""
        if value is None:
            return 0
        if isinstance(value, (int, float)):
            return value
        if isinstance(value, str):
            # Handle percentage values
            if '%' in value:
                try:
                    return float(value.replace('%', ''))
                except (ValueError, TypeError):
                    return 0.0
            # Handle numeric strings
            try:
                return int(value)
            except (ValueError, TypeError):
                try:
                    return float(value)
                except (ValueError, TypeError):
                    return 0
        return 0
