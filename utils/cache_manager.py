import json
import os
import hashlib
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging


class OrganizedCacheManager:
    def __init__(self, cache_dir: str = "api_cache", ttl: int = 3600):
        self.logger = logging.getLogger(__name__)
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache_file = os.path.join(cache_dir, "organized_cache.json")
        self._ensure_cache_dir()
        self._load_cache()

    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _load_cache(self):
        """Load the organized cache from file"""
        if not os.path.exists(self.cache_file):
            self.cache_data = {
                'leagues': {},
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'last_updated': datetime.now().isoformat(),
                    'total_matches': 0,
                    'total_leagues': 0
                }
            }
            self._save_cache()
        else:
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache_data = json.load(f)
                self.logger.info("Loaded organized cache from file")
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.warning(f"Failed to load cache, creating new: {e}")
                self.cache_data = {
                    'leagues': {},
                    'metadata': {
                        'created_at': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat(),
                        'total_matches': 0,
                        'total_leagues': 0
                    }
                }

    def _save_cache(self):
        """Save the organized cache to file"""
        try:
            self.cache_data['metadata']['last_updated'] = datetime.now().isoformat()

            # Create backup before saving
            if os.path.exists(self.cache_file):
                backup_file = self.cache_file + '.backup'
                os.replace(self.cache_file, backup_file)

            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            self.logger.error(f"Failed to save cache: {e}")

    def save_league_info(self, league_id: int, league_data: Dict[str, Any]):
        """Save league information"""
        if 'leagues' not in self.cache_data:
            self.cache_data['leagues'] = {}

        if str(league_id) not in self.cache_data['leagues']:
            self.cache_data['leagues'][str(league_id)] = {
                'info': league_data,
                'seasons': {}
            }
            self._save_cache()

    def save_matches(self, league_id: int, season: int, matches_data: List[Dict[str, Any]]):
        """Save matches for a league and season"""
        league_key = str(league_id)
        season_key = str(season)

        # Ensure league exists
        if league_key not in self.cache_data['leagues']:
            self.cache_data['leagues'][league_key] = {
                'info': {},
                'seasons': {}
            }

        # Ensure season exists
        if season_key not in self.cache_data['leagues'][league_key]['seasons']:
            self.cache_data['leagues'][league_key]['seasons'][season_key] = {
                'matches': {}
            }

        # Save each match
        for match_data in matches_data:
            match_id = match_data['fixture']['id']
            self.cache_data['leagues'][league_key]['seasons'][season_key]['matches'][str(match_id)] = {
                'basic_info': {
                    'home_team': match_data['teams']['home']['name'],
                    'away_team': match_data['teams']['away']['name'],
                    'score_home': match_data['goals']['home'],
                    'score_away': match_data['goals']['away'],
                    'date': match_data['fixture']['date']
                },
                'fixture_data': match_data,  # Store the complete fixture data
                'saved_at': datetime.now().isoformat()  # Track when match was saved
            }

        # Update total matches count
        self.cache_data['metadata']['total_matches'] = self._count_processed_matches()
        self._save_cache()

    def save_match_details(self, league_id: int, season: int, match_id: int,
                           events: List[Dict], statistics: List[Dict]):
        """Save detailed match data (events and statistics)"""
        league_key = str(league_id)
        season_key = str(season)
        match_key = str(match_id)

        try:
            if (league_key in self.cache_data['leagues'] and
                    season_key in self.cache_data['leagues'][league_key]['seasons'] and
                    match_key in self.cache_data['leagues'][league_key]['seasons'][season_key]['matches']):
                match_data = self.cache_data['leagues'][league_key]['seasons'][season_key]['matches'][match_key]
                match_data['events'] = events
                match_data['statistics'] = statistics
                match_data['has_details'] = True  # Mark as having details
                match_data['last_updated'] = datetime.now().isoformat()

                self.logger.info(f"💾 Cached details for match {match_id}")
                self._save_cache()

        except KeyError as e:
            self.logger.warning(f"Could not save details for match {match_id}: {e}")

    def get_league_matches(self, league_id: int, season: int) -> Optional[Dict[str, Any]]:
        """Get all matches for a league and season"""
        league_key = str(league_id)
        season_key = str(season)

        try:
            return self.cache_data['leagues'][league_key]['seasons'][season_key]['matches']
        except KeyError:
            return None

    def get_match_details(self, league_id: int, season: int, match_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed match data"""
        league_key = str(league_id)
        season_key = str(season)
        match_key = str(match_id)

        try:
            match_data = self.cache_data['leagues'][league_key]['seasons'][season_key]['matches'][match_key]
            if match_data.get('has_details'):
                self.logger.debug(f"📦 Cache HIT for match {match_id}")
                return match_data
            else:
                self.logger.debug(f"📦 Cache MISS (no details) for match {match_id}")
        except KeyError:
            self.logger.debug(f"📦 Cache MISS (not found) for match {match_id}")
        return None

    def _count_processed_matches(self) -> int:
        """Count total matches across all leagues and seasons (not just processed ones)"""
        count = 0
        for league_data in self.cache_data['leagues'].values():
            for season_data in league_data.get('seasons', {}).values():
                count += len(season_data.get('matches', {}))
        return count

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_leagues = len(self.cache_data['leagues'])
        total_seasons = sum(len(league['seasons']) for league in self.cache_data['leagues'].values())
        total_matches = sum(
            len(season['matches'])
            for league in self.cache_data['leagues'].values()
            for season in league['seasons'].values()
        )

        return {
            'total_leagues': total_leagues,
            'total_seasons': total_seasons,
            'total_matches': total_matches,
            'processed_matches': self.cache_data['metadata']['total_matches'],
            'created_at': self.cache_data['metadata']['created_at'],
            'last_updated': self.cache_data['metadata']['last_updated']
        }

    def clear_expired(self):
        """Clear expired cache entries (not implemented for organized cache)"""
        # For organized cache, we don't implement TTL per entry
        # You can implement this if needed
        pass

    def clear_all(self):
        """Clear all cache data"""
        self.cache_data = {
            'leagues': {},
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_matches': 0,
                'total_leagues': 0
            }
        }
        self._save_cache()
        self.logger.info("Cleared all cache data")