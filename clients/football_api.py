import requests
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import logging
from config.settings import APIConfig
from data.models import Match, MatchEvent, EventType


class APIFootballClient:
    def __init__(self, config: APIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'x-apisports-key': config.API_KEY
        })
        self.logger = logging.getLogger(__name__)
        self.last_request_time = 0

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
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {e}")
            return None

    def get_leagues(self) -> List[Dict[str, Any]]:
        """Get available leagues"""
        return self._make_request("leagues", {})

    def get_teams(self, league_id: int, season: int) -> List[Dict[str, Any]]:
        """Get teams for a league and season"""
        params = {'league': league_id, 'season': season}
        return self._make_request("teams", params)

    def get_matches(self, league_id: int, season: int) -> List[Dict[str, Any]]:
        """Get matches for a league and season"""
        params = {'league': league_id, 'season': season}
        return self._make_request("fixtures", params)

    def get_match_events(self, match_id: int) -> List[Dict[str, Any]]:
        """Get events for a specific match"""
        params = {'fixture': match_id}
        return self._make_request("fixtures/events", params)

    def get_match_statistics(self, match_id: int) -> List[Dict[str, Any]]:
        """Get statistics for a specific match"""
        params = {'fixture': match_id}
        return self._make_request("fixtures/statistics", params)

    def parse_match_data(self, match_data: Dict[str, Any]) -> Match:
        """Parse raw match data into Match object"""
        # This is a simplified parser - you'd expand this based on API response structure
        events = self._extract_events(match_data)

        return Match(
            id=match_data['fixture']['id'],
            league=match_data['league']['name'],
            season=match_data['league']['season'],
            date=match_data['fixture']['date'],
            home_team=match_data['teams']['home']['name'],
            away_team=match_data['teams']['away']['name'],
            score_home=match_data['goals']['home'] or 0,
            score_away=match_data['goals']['away'] or 0,
            events=events
        )

    def _extract_events(self, match_data: Dict[str, Any]) -> List[MatchEvent]:
        """Extract various events from match data"""
        events = []

        # Extract goals
        events.extend(self._extract_goal_events(match_data))

        # Extract cards
        events.extend(self._extract_card_events(match_data))

        # Extract other statistics
        events.extend(self._extract_statistical_events(match_data))

        return events

    def _extract_goal_events(self, match_data: Dict[str, Any]) -> List[MatchEvent]:
        """Extract goal-related events"""
        events = []
        home_score = match_data['goals']['home'] or 0
        away_score = match_data['goals']['away'] or 0

        # Total goals
        events.append(MatchEvent(EventType.GOALS, home_score + away_score))

        # Home/Away goals
        events.append(MatchEvent(EventType.GOALS, home_score, is_home=True))
        events.append(MatchEvent(EventType.GOALS, away_score, is_home=False))

        return events

    def _extract_card_events(self, match_data: Dict[str, Any]) -> List[MatchEvent]:
        """Extract card-related events"""
        events = []
        # This would parse actual card events from the API
        # For now, using placeholder logic
        return events

    def _extract_statistical_events(self, match_data: Dict[str, Any]) -> List[MatchEvent]:
        """Extract various statistical events"""
        events = []
        # This would parse statistics like shots, corners, possession, etc.
        return events
