import json
import os
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime
import logging


class ProgressManager:
    """Manages progress tracking and resumption for combination analysis"""

    def __init__(self, progress_file: str = "analysis_progress.json"):
        self.progress_file = progress_file
        self.logger = logging.getLogger(__name__)
        self.current_state: Dict[str, Any] = {}

    def load_progress(self) -> Optional[Dict[str, Any]]:
        """Load progress from file"""
        if not os.path.exists(self.progress_file):
            return None

        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                progress = json.load(f)
            self.logger.info("Loaded progress from file")
            return progress
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.warning(f"Failed to load progress: {e}")
            return None

    def save_progress(self,
                      league_id: int,
                      season: int,
                      combination_size: int,
                      current_combination: Tuple[str, ...],
                      total_combinations: int,
                      processed_combinations: int):
        """Save current progress"""
        progress = {
            'timestamp': datetime.now().isoformat(),
            'league_id': league_id,
            'season': season,
            'combination_size': combination_size,
            'current_combination': current_combination,
            'total_combinations': total_combinations,
            'processed_combinations': processed_combinations
        }

        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
            self.current_state = progress
        except Exception as e:
            self.logger.error(f"Failed to save progress: {e}")

    def get_resume_point(self, league_id: int, season: int, combination_size: int) -> Optional[Tuple[str, ...]]:
        """Get the combination to resume from"""
        progress = self.load_progress()
        if not progress:
            return None

        if (progress.get('league_id') == league_id and
                progress.get('season') == season and
                progress.get('combination_size') == combination_size):
            return tuple(progress.get('current_combination', []))

        return None

    def clear_progress(self):
        """Clear progress file"""
        if os.path.exists(self.progress_file):
            os.remove(self.progress_file)
            self.logger.info("Cleared progress file")