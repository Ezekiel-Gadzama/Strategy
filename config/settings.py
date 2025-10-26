import os
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class APIConfig:
    BASE_URL: str = "https://v3.football.api-sports.io/"
    API_KEY: str = os.getenv("API_FOOTBALL_KEY", "875e287371ab75de8e3ece04bdbd3bf3")
    RATE_LIMIT: int = 10  # requests per minute
    TIMEOUT: int = 30
    CACHE_TTL: int = 3600 * 4


@dataclass
class AnalysisConfig:
    MIN_EVENTS_COMBINATION: int = 3
    MAX_EVENTS_COMBINATION: int = 5
    MAX_RESULTS_PER_CATEGORY: int = 20
    COMBINATION_STRATEGY: str = "by_event_type"  # "by_event_type", "by_market", "full"
    MIN_OCCURRENCE_THRESHOLD: float = 0.001  # 0.1%
    LEAGUES: List[str] = field(default_factory=lambda: [
        "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
        "Champions League", "Europa League", "Eredivisie", "Primeira Liga"
    ])
    SEASON: List[int] = field(default_factory=lambda: [2022, 2023, 2024])
    PAST_YEARS: int = 1
    THREAD_COUNT: int = 3  # Number of threads for parallel processing


@dataclass
class Config:
    api: APIConfig = field(default_factory=APIConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)