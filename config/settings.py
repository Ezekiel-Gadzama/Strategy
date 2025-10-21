import os
from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class APIConfig:
    BASE_URL: str = "https://v3.football.api-sports.io/"
    API_KEY: str = os.getenv("API_FOOTBALL_KEY", "54cbc9ceee66b541b1a2a1066ac2499c")
    RATE_LIMIT: int = 10  # requests per minute
    TIMEOUT: int = 30


@dataclass
class AnalysisConfig:
    MIN_EVENTS_COMBINATION: int = 3
    MAX_EVENTS_COMBINATION: int = 5
    MIN_OCCURRENCE_THRESHOLD: float = 0.001  # 0.1%
    LEAGUES: List[str] = field(default_factory=lambda: [
        "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1",
        "Champions League", "Europa League", "Eredivisie", "Primeira Liga"
    ])
    SEASON: int = 2023
    PAST_YEARS: int = 1


@dataclass
class Config:
    api: APIConfig = field(default_factory=APIConfig)
    analysis: AnalysisConfig = field(default_factory=AnalysisConfig)
