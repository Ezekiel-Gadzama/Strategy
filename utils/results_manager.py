import json
import os
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime
import logging
from pathlib import Path


class ResultsManager:
    """Manages comprehensive results storage and resumption for combination analysis"""

    def __init__(self, results_file: str = "comprehensive_results.json"):
        # Create results directory if it doesn't exist
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)

        # Set the results file path inside the results directory
        self.results_file = self.results_dir / results_file

        self.logger = logging.getLogger(__name__)
        self.results_data = self._load_results()

    def _load_results(self) -> Dict[str, Any]:
        """Load results from file, fall back to backup if main file is corrupted"""
        backup_file = self.results_file.with_suffix('.json.backup')

        # Try to load the main file first
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.logger.info("Successfully loaded results from main file")
                    return data
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.warning(f"Main results file corrupted: {e}")
                # Main file is corrupted, try backup
                if os.path.exists(backup_file):
                    try:
                        with open(backup_file, 'r', encoding='utf-8') as f:
                            backup_data = json.load(f)
                        self.logger.info("Successfully loaded results from backup file")
                        print("Successfully loaded results from backup file")

                        # Restore the backup to main file
                        try:
                            with open(self.results_file, 'w', encoding='utf-8') as f:
                                json.dump(backup_data, f, indent=2, ensure_ascii=False)
                            self.logger.info("Restored backup to main file")
                        except Exception as restore_error:
                            self.logger.warning(f"Could not restore backup: {restore_error}")

                        return backup_data
                    except (json.JSONDecodeError, KeyError) as backup_error:
                        self.logger.error(f"Backup file also corrupted: {backup_error}")
                        # Both files are corrupted, create new
                        return self._create_new_results()
                else:
                    self.logger.warning("No backup file found, creating new results")
                    return self._create_new_results()

        # Try backup if main file doesn't exist
        elif os.path.exists(backup_file):
            try:
                with open(backup_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.logger.info("Loaded results from backup file (main file missing)")

                # Restore backup to main file
                try:
                    with open(self.results_file, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=2, ensure_ascii=False)
                    self.logger.info("Restored backup to main file")
                except Exception as restore_error:
                    self.logger.warning(f"Could not restore backup: {restore_error}")

                return data
            except (json.JSONDecodeError, KeyError) as e:
                self.logger.error(f"Backup file corrupted: {e}")
                return self._create_new_results()

        # No files exist, create new
        else:
            self.logger.info("No results files found, creating new")
            return self._create_new_results()

    def _create_new_results(self) -> Dict[str, Any]:
        """Create a new results structure"""
        return {
            'leagues': {},
            'metadata': {
                'created_at': datetime.now().isoformat(),
                'last_updated': datetime.now().isoformat(),
                'total_leagues': 0,
                'total_seasons': 0
            }
        }

    def _save_results(self):
        """Simple save without atomic operations"""
        try:
            self.results_data['metadata']['last_updated'] = datetime.now().isoformat()

            # Optional: Create backup (without atomic operations)
            backup_file = self.results_file.with_suffix('.json.backup')
            if os.path.exists(self.results_file):
                try:
                    import shutil
                    shutil.copy2(self.results_file, backup_file)
                except Exception as backup_error:
                    self.logger.warning(f"Could not create backup: {backup_error}")

            # Direct write (no temp file)
            with open(self.results_file, 'w', encoding='utf-8') as f:
                json.dump(self.results_data, f, indent=2, ensure_ascii=False)

            self.logger.debug("Results saved successfully")

        except Exception as e:
            self.logger.error(f"Failed to save results: {e}")

    def initialize_league_season(self, league_id: int, league_name: str, season: int, total_matches: int):
        """Initialize a new league/season entry"""
        league_key = str(league_id)
        season_key = str(season)

        if league_key not in self.results_data['leagues']:
            self.results_data['leagues'][league_key] = {
                'name': league_name,
                'seasons': {}
            }

        if season_key not in self.results_data['leagues'][league_key]['seasons']:
            self.results_data['leagues'][league_key]['seasons'][season_key] = {
                'total_matches_processed': total_matches,
                'combos': {},
                'analysis_results': {},
                'current_progress': {
                    'combination_size': None,
                    'current_combination': None,
                    'processed_count': 0,
                    'total_combinations': 0,
                    'last_updated': datetime.now().isoformat()
                }
            }

            # Update metadata
            self.results_data['metadata']['total_leagues'] = len(self.results_data['leagues'])
            self.results_data['metadata']['total_seasons'] = sum(
                len(league['seasons']) for league in self.results_data['leagues'].values()
            )

            self._save_results()

    def save_combo_result(self, league_id: int, season: int, combo: Tuple[str, ...], occurrence_count: int,
                          total_matches: int, defer_save: bool = False):
        """Save combination result with optional deferred saving"""
        league_key = str(league_id)
        season_key = str(season)
        combo_key = ','.join(combo)

        try:
            if (league_key in self.results_data['leagues'] and
                    season_key in self.results_data['leagues'][league_key]['seasons']):
                season_data = self.results_data['leagues'][league_key]['seasons'][season_key]
                season_data['combos'][combo_key] = {
                    'appeared_count': occurrence_count,
                    'percentage': (occurrence_count / total_matches) * 100 if total_matches > 0 else 0.0,
                    'combination_size': len(combo),
                    'last_updated': datetime.now().isoformat()
                }

                if not defer_save:
                    print("trying to save")
                    self._save_results()
                    print("saved result")

        except KeyError as e:
            self.logger.warning(f"Could not save combo result: {e}")

    def update_progress(self, league_id: int, season: int, combination_size: int,
                        current_combination: Tuple[str], processed_count: int, total_combinations: int):
        """Update progress for current analysis"""
        league_key = str(league_id)
        season_key = str(season)

        try:
            if (league_key in self.results_data['leagues'] and
                    season_key in self.results_data['leagues'][league_key]['seasons']):
                season_data = self.results_data['leagues'][league_key]['seasons'][season_key]
                season_data['current_progress'] = {
                    'combination_size': combination_size,
                    'current_combination': list(current_combination),  # Convert tuple to list for JSON
                    'processed_count': processed_count,
                    'total_combinations': total_combinations,
                    'last_updated': datetime.now().isoformat()
                }

                # DEBUG: Print what we're saving
                print(f"💾 SAVING PROGRESS: {league_key} {season_key}, size {combination_size}")
                print(f"💾 Current combo: {current_combination}")
                print(f"💾 Processed: {processed_count}/{total_combinations}")

                self._save_results()

        except KeyError as e:
            self.logger.warning(f"Could not update progress: {e}")

    def get_resume_point(self, league_id: int, season: int) -> Optional[Dict[str, Any]]:
        """Get resume point for league/season"""
        league_key = str(league_id)
        season_key = str(season)

        try:
            if (league_key in self.results_data['leagues'] and
                    season_key in self.results_data['leagues'][league_key]['seasons']):

                progress = self.results_data['leagues'][league_key]['seasons'][season_key]['current_progress']
                if progress['current_combination']:
                    # DEBUG: Print what we found
                    print(f"🔍 FOUND RESUME POINT: {progress}")
                    return progress

        except KeyError:
            pass

        print("🔍 NO RESUME POINT FOUND")
        return None

    def save_analysis_results(self, league_id: int, season: int, analysis_results: Dict[str, Any]):
        """Save final analysis results for a league/season"""
        league_key = str(league_id)
        season_key = str(season)

        try:
            if (league_key in self.results_data['leagues'] and
                    season_key in self.results_data['leagues'][league_key]['seasons']):
                season_data = self.results_data['leagues'][league_key]['seasons'][season_key]
                season_data['analysis_results'] = analysis_results

                # Clear progress since analysis is complete
                season_data['current_progress'] = {
                    'combination_size': None,
                    'current_combination': None,
                    'processed_count': 0,
                    'total_combinations': 0,
                    'last_updated': datetime.now().isoformat()
                }

                self._save_results()

        except KeyError as e:
            self.logger.warning(f"Could not save analysis results: {e}")

    def get_all_results(self) -> Dict[str, Any]:
        """Get all results"""
        return self.results_data

    def get_league_season_results(self, league_id: int, season: int) -> Optional[Dict[str, Any]]:
        """Get results for specific league/season"""
        league_key = str(league_id)
        season_key = str(season)

        try:
            return self.results_data['leagues'][league_key]['seasons'][season_key]
        except KeyError:
            return None
