import json
from typing import Any, Dict, List
from datetime import datetime


def save_results(results: Dict[str, Any], filename: str):
    """Save analysis results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2, default=str)


def format_percentage(value: float) -> str:
    """Format percentage with 2 decimal places"""
    return f"{value:.2f}%"


def get_season_years(current_year: int, past_years: int = 1) -> List[int]:
    """Get list of seasons to analyze"""
    return list(range(current_year - past_years, current_year + 1))
