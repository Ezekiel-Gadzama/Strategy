import json
import os
import hashlib
from typing import Dict, Any, Optional, List, Set
from datetime import datetime
import logging


class UnifiedCacheManager:
    """Unified cache manager that stores all data in a single file"""

    def __init__(self, cache_dir: str = "api_cache", ttl: int = 3600):
        self.logger = logging.getLogger(__name__)
        self.cache_dir = cache_dir
        self.ttl = ttl
        self.cache_file = os.path.join(cache_dir, "unified_cache.json")
        self._ensure_cache_dir()
        self._load_cache()

    def _ensure_cache_dir(self):
        """Create cache directory if it doesn't exist"""
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

    def _load_cache(self):
        """Load the unified cache from file"""
        if not os.path.exists(self.cache_file):
            self.cache_data = {
                'api_responses': {},
                'match_data': {},
                'metadata': {
                    'created_at': datetime.now().isoformat(),
                    'last_updated': datetime.now().isoformat(),
                    'total_matches': 0,
                    'total_api_calls': 0
                }
            }
            self._save_cache()
        else:
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    self.cache_data = json.load(f)
                self.logger.info("Loaded unified cache from file")
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.warning(f"Failed to load cache, creating new: {e}")
                self.cache_data = {
                    'api_responses': {},
                    'match_data': {},
                    'metadata': {
                        'created_at': datetime.now().isoformat(),
                        'last_updated': datetime.now().isoformat(),
                        'total_matches': 0,
                        'total_api_calls': 0
                    }
                }

    def _save_cache(self):
        """Save the unified cache to file"""
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

    def _get_api_cache_key(self, endpoint: str, params: Dict[str, Any]) -> str:
        """Generate a unique cache key for API requests"""
        key_string = f"{endpoint}:{json.dumps(params, sort_keys=True)}"
        return hashlib.md5(key_string.encode()).hexdigest()

    def _is_expired(self, timestamp: str) -> bool:
        """Check if cache entry is expired"""
        cache_time = datetime.fromisoformat(timestamp)
        current_time = datetime.now()
        time_diff = (current_time - cache_time).total_seconds()
        return time_diff > self.ttl

    def get_api_response(self, endpoint: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached API response"""
        cache_key = self._get_api_cache_key(endpoint, params)

        if cache_key in self.cache_data['api_responses']:
            cached_entry = self.cache_data['api_responses'][cache_key]

            if not self._is_expired(cached_entry['timestamp']):
                self.logger.debug(f"Using cached API response for {endpoint}")
                return cached_entry['response']
            else:
                # Remove expired entry
                del self.cache_data['api_responses'][cache_key]
                self._save_cache()

        return None

    def set_api_response(self, endpoint: str, params: Dict[str, Any], response: Dict[str, Any]):
        """Cache API response"""
        cache_key = self._get_api_cache_key(endpoint, params)

        self.cache_data['api_responses'][cache_key] = {
            'timestamp': datetime.now().isoformat(),
            'endpoint': endpoint,
            'params': params,
            'response': response
        }
        self.cache_data['metadata']['total_api_calls'] += 1
        self._save_cache()
        self.logger.debug(f"Cached API response for {endpoint}")

    def get_match_data(self, match_id: int) -> Optional[Dict[str, Any]]:
        """Get cached match data"""
        match_key = str(match_id)

        if match_key in self.cache_data['match_data']:
            cached_entry = self.cache_data['match_data'][match_key]

            if not self._is_expired(cached_entry['timestamp']):
                self.logger.debug(f"Using cached match data for match {match_id}")
                return cached_entry['data']
            else:
                # Remove expired entry
                del self.cache_data['match_data'][match_key]
                self._save_cache()

        return None

    def set_match_data(self, match_id: int, match_data: Dict[str, Any]):
        """Cache match data"""
        match_key = str(match_id)

        self.cache_data['match_data'][match_key] = {
            'timestamp': datetime.now().isoformat(),
            'match_id': match_id,
            'data': match_data
        }
        self.cache_data['metadata']['total_matches'] = len(self.cache_data['match_data'])
        self._save_cache()
        self.logger.debug(f"Cached match data for match {match_id}")

    def get_all_match_ids(self) -> Set[int]:
        """Get all cached match IDs"""
        return set(int(match_id) for match_id in self.cache_data['match_data'].keys())

    def clear_expired(self):
        """Clear all expired cache entries"""
        current_time = datetime.now()
        expired_count = 0

        # Check API responses
        api_keys_to_remove = []
        for cache_key, entry in self.cache_data['api_responses'].items():
            if self._is_expired(entry['timestamp']):
                api_keys_to_remove.append(cache_key)
                expired_count += 1

        for key in api_keys_to_remove:
            del self.cache_data['api_responses'][key]

        # Check match data
        match_keys_to_remove = []
        for match_key, entry in self.cache_data['match_data'].items():
            if self._is_expired(entry['timestamp']):
                match_keys_to_remove.append(match_key)
                expired_count += 1

        for key in match_keys_to_remove:
            del self.cache_data['match_data'][key]

        if expired_count > 0:
            self.cache_data['metadata']['total_matches'] = len(self.cache_data['match_data'])
            self._save_cache()
            self.logger.info(f"Cleared {expired_count} expired cache entries")

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            'total_matches': len(self.cache_data['match_data']),
            'total_api_responses': len(self.cache_data['api_responses']),
            'created_at': self.cache_data['metadata']['created_at'],
            'last_updated': self.cache_data['metadata']['last_updated'],
            'cache_size_mb': os.path.getsize(self.cache_file) / (1024 * 1024) if os.path.exists(self.cache_file) else 0
        }

    def clear_all(self):
        """Clear all cache data"""
        self.cache_data = {
            'api_responses': {},
            'match_data': {},
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_matches': 0,
                'total_api_calls': 0
            }
        }
        self._save_cache()
        self.logger.info("Cleared all cache data")