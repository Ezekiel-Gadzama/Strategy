import requests
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from config.settings import APIConfig
from data.models import Match, MatchEvent, EventType, TeamStats, HalfStats
from utils.cache_manager import UnifiedCacheManager


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
        # Use unified cache manager
        self.cache = UnifiedCacheManager(cache_dir="api_cache", ttl=config.CACHE_TTL)

        # Clear expired cache on initialization
        self.cache.clear_expired()

    def _rate_limit(self):
        """Implement rate limiting"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        min_interval = 60 / self.config.RATE_LIMIT

        if time_since_last < min_interval:
            time.sleep(min_interval - time_since_last)
        self.last_request_time = time.time()

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make API request with error handling and caching"""
        # Try to get from cache first
        cached_response = self.cache.get_api_response(endpoint, params)  # FIXED: Changed to get_api_response
        if cached_response is not None:
            return cached_response

        # If not in cache, make API request
        self._rate_limit()

        try:
            url = f"{self.config.BASE_URL}/{endpoint}"
            response = self.session.get(url, params=params, timeout=self.config.TIMEOUT)
            response.raise_for_status()
            api_response = response.json()

            # Cache the successful response
            self.cache.set_api_response(endpoint, params, api_response)  # FIXED: Changed to set_api_response

            return api_response

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed for {endpoint}: {e}")
            return None

    def get_leagues(self) -> List[Dict[str, Any]]:
        """Get available leagues"""
        response = self._make_request("leagues", {"current": "true"})
        return response.get("response", []) if response else []

    def get_matches(self, league_id: int, season: int, round: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get matches for a league and season"""
        params = {'league': league_id, 'season': season}
        if round:
            params['round'] = round

        response = self._make_request("fixtures", params)
        return response.get("response", []) if response else []

    def get_match_events(self, match_id: int) -> List[Dict[str, Any]]:
        """Get events for a specific match - check cache first"""
        # First check if we have processed match data
        cached_match = self.cache.get_match_data(match_id)
        if cached_match and 'events' in cached_match:
            return cached_match['events']

        # If not, check API cache for raw events
        params = {'fixture': match_id}
        cached_response = self.cache.get_api_response("fixtures/events", params)
        if cached_response:
            return cached_response.get("response", [])

        # If not in cache, make API request
        response = self._make_request("fixtures/events", params)
        return response.get("response", []) if response else []

    def get_match_statistics(self, match_id: int) -> List[Dict[str, Any]]:
        """Get statistics for a specific match - check cache first"""
        cached_match = self.cache.get_match_data(match_id)
        if cached_match and 'statistics' in cached_match:  # FIXED: Removed ['data']
            return cached_match['statistics']  # FIXED: Removed ['data']

        # Also check API cache for raw statistics
        params = {'fixture': match_id}
        cached_response = self.cache.get_api_response("fixtures/statistics", params)
        if cached_response:
            return cached_response.get("response", [])

        # If not in cache, make API request
        response = self._make_request("fixtures/statistics", params)
        return response.get("response", []) if response else []

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
        # Check if we have complete cached match data
        cached_match = self.cache.get_match_data(match.id)
        if cached_match and cached_match.get('complete'):
            # Load from cache
            self._load_match_from_cache(match, cached_match)
            return

        # Get match events
        events_data = self.get_match_events(match.id)
        self._process_events(match, events_data)

        # Get match statistics
        stats_data = self.get_match_statistics(match.id)
        self._process_statistics(match, stats_data)

        # Extract half-time statistics from events
        self._extract_half_stats(match, events_data)

        # Generate derived events for pattern analysis
        self._generate_derived_events(match)

        # Cache the complete match data
        self._cache_complete_match(match)

    def _load_match_from_cache(self, match: Match, cached_data: Dict[str, Any]):
        """Load match data from cache with proper parameter handling"""
        match.events = []
        for event_dict in cached_data.get('events', []):
            try:
                # Handle both 'type' and 'event_type' parameter names
                if 'type' in event_dict and 'event_type' not in event_dict:
                    event_dict = event_dict.copy()
                    event_dict['event_type'] = event_dict.pop('type')

                # Convert string event_type back to EventType enum
                if isinstance(event_dict.get('event_type'), str):
                    event_dict['event_type'] = EventType(event_dict['event_type'])

                event = MatchEvent(**event_dict)
                match.events.append(event)
            except Exception as e:
                self.logger.warning(f"Failed to load event from cache: {e}")
                continue

        # Rest of the loading code for stats...
        if cached_data.get('home_stats'):
            match.home_stats = TeamStats(**cached_data['home_stats'])
        if cached_data.get('away_stats'):
            match.away_stats = TeamStats(**cached_data['away_stats'])
        if cached_data.get('first_half'):
            match.first_half = HalfStats(**cached_data['first_half'])
        if cached_data.get('second_half'):
            match.second_half = HalfStats(**cached_data['second_half'])

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

        if event_type in ['Goal', 'Penalty', 'Missed Penalty']:
            return EventType.GOALS
        elif event_type in ['Card', 'Yellow Card', 'Red Card']:
            return EventType.CARDS
        elif event_type == 'Corner':
            return EventType.CORNERS
        elif event_type == 'Subst':
            return EventType.TEAM_STATS
        elif event_type == 'Var':
            return EventType.TEAM_STATS
        elif event_type == 'Foul':
            return EventType.FOULS
        elif event_type == 'Offside':
            return EventType.OFFSIDES

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
