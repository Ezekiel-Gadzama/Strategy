from typing import List, Callable, Tuple
from dataclasses import dataclass
from data.models import Match, EventType


@dataclass
class EventCondition:
    name: str
    description: str
    market: str
    event_type: EventType
    condition: Callable[[Match], bool]


class EventPatterns:
    """Define various event patterns (markets) to analyze"""

    @staticmethod
    def get_all_patterns() -> List[EventCondition]:
        return [
            # =============================================================
            # --- GOALS MARKETS ---
            # =============================================================

            # --- total_goals_exact ---
            EventCondition("total_goals_0", "Total goals = 0", "total_goals_exact", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 0),
            EventCondition("total_goals_1", "Total goals = 1", "total_goals_exact", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 1),
            EventCondition("total_goals_2", "Total goals = 2", "total_goals_exact", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 2),
            EventCondition("total_goals_3", "Total goals = 3", "total_goals_exact", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 3),
            EventCondition("total_goals_4", "Total goals = 4", "total_goals_exact", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 4),
            EventCondition("total_goals_5_plus", "Total goals ≥ 5", "total_goals_exact", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) >= 5),

            # --- total_goals_over_under ---
            EventCondition("over_0_5_goals", "Total goals over 0.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) > 0.5),
            EventCondition("over_1_5_goals", "Total goals over 1.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) > 1.5),
            EventCondition("over_2_5_goals", "Total goals over 2.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) > 2.5),
            EventCondition("over_3_5_goals", "Total goals over 3.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) > 3.5),
            EventCondition("over_4_5_goals", "Total goals over 4.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) > 4.5),
            EventCondition("over_5_5_goals", "Total goals over 5.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) > 5.5),
            EventCondition("under_0_5_goals", "Total goals under 0.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) < 0.5),
            EventCondition("under_1_5_goals", "Total goals under 1.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) < 1.5),
            EventCondition("under_2_5_goals", "Total goals under 2.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) < 2.5),
            EventCondition("under_3_5_goals", "Total goals under 3.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) < 3.5),
            EventCondition("under_4_5_goals", "Total goals under 4.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) < 4.5),
            EventCondition("under_5_5_goals", "Total goals under 5.5", "total_goals_over_under", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) < 5.5),

            # --- btts ---
            EventCondition("btts_yes", "Both teams to score (Yes)", "btts", EventType.GOALS,
                           lambda m: m.score_home > 0 and m.score_away > 0),
            EventCondition("btts_no", "Both teams to score (No)", "btts", EventType.GOALS,
                           lambda m: m.score_home == 0 or m.score_away == 0),

            # --- clean_sheet ---
            EventCondition("clean_sheet_home", "Home team clean sheet", "clean_sheet", EventType.GOALS,
                           lambda m: m.score_away == 0),
            EventCondition("clean_sheet_away", "Away team clean sheet", "clean_sheet", EventType.GOALS,
                           lambda m: m.score_home == 0),

            # --- win_to_nil ---
            EventCondition("home_win_to_nil", "Home team win to nil", "win_to_nil", EventType.GOALS,
                           lambda m: m.score_home > 0 and m.score_away == 0),
            EventCondition("away_win_to_nil", "Away team win to nil", "win_to_nil", EventType.GOALS,
                           lambda m: m.score_away > 0 and m.score_home == 0),

            # --- team_total_goals ---
            EventCondition("home_over_0_5", "Home team over 0.5 goals", "team_total_goals_home", EventType.GOALS,
                           lambda m: m.score_home > 0.5),
            EventCondition("home_over_1_5", "Home team over 1.5 goals", "team_total_goals_home", EventType.GOALS,
                           lambda m: m.score_home > 1.5),
            EventCondition("home_over_2_5", "Home team over 2.5 goals", "team_total_goals_home", EventType.GOALS,
                           lambda m: m.score_home > 2.5),
            EventCondition("away_over_0_5", "Away team over 0.5 goals", "team_total_goals_away", EventType.GOALS,
                           lambda m: m.score_away > 0.5),
            EventCondition("away_over_1_5", "Away team over 1.5 goals", "team_total_goals_away", EventType.GOALS,
                           lambda m: m.score_away > 1.5),
            EventCondition("away_over_2_5", "Away team over 2.5 goals", "team_total_goals_away", EventType.GOALS,
                           lambda m: m.score_away > 2.5),

            # --- goal_range ---
            EventCondition("goal_range_0_1", "Goal range 0-1", "goal_range", EventType.GOALS,
                           lambda m: 0 <= (m.score_home + m.score_away) <= 1),
            EventCondition("goal_range_2_3", "Goal range 2-3", "goal_range", EventType.GOALS,
                           lambda m: 2 <= (m.score_home + m.score_away) <= 3),
            EventCondition("goal_range_4_6", "Goal range 4-6", "goal_range", EventType.GOALS,
                           lambda m: 4 <= (m.score_home + m.score_away) <= 6),
            EventCondition("goal_range_7_plus", "Goal range 7+", "goal_range", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) >= 7),

            # --- teams_to_score ---
            EventCondition("teams_to_score_none", "No team scores", "teams_to_score", EventType.GOALS,
                           lambda m: m.score_home == 0 and m.score_away == 0),
            EventCondition("teams_to_score_only_home", "Only home team scores", "teams_to_score", EventType.GOALS,
                           lambda m: m.score_home > 0 and m.score_away == 0),
            EventCondition("teams_to_score_only_away", "Only away team scores", "teams_to_score", EventType.GOALS,
                           lambda m: m.score_away > 0 and m.score_home == 0),
            EventCondition("teams_to_score_both", "Both teams score", "teams_to_score", EventType.GOALS,
                           lambda m: m.score_home > 0 and m.score_away > 0),

            # --- odd_even ---
            EventCondition("total_goals_odd", "Total goals odd", "odd_even", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) % 2 == 1),
            EventCondition("total_goals_even", "Total goals even", "odd_even", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) % 2 == 0),
            EventCondition("home_goals_odd", "Home team goals odd", "odd_even", EventType.GOALS,
                           lambda m: m.score_home % 2 == 1),
            EventCondition("home_goals_even", "Home team goals even", "odd_even", EventType.GOALS,
                           lambda m: m.score_home % 2 == 0),
            EventCondition("away_goals_odd", "Away team goals odd", "odd_even", EventType.GOALS,
                           lambda m: m.score_away % 2 == 1),
            EventCondition("away_goals_even", "Away team goals even", "odd_even", EventType.GOALS,
                           lambda m: m.score_away % 2 == 0),

            # --- exact_goals_home ---
            EventCondition("home_goals_0", "Home team 0 goals", "exact_goals_home", EventType.GOALS,
                           lambda m: m.score_home == 0),
            EventCondition("home_goals_1", "Home team 1 goal", "exact_goals_home", EventType.GOALS,
                           lambda m: m.score_home == 1),
            EventCondition("home_goals_2", "Home team 2 goals", "exact_goals_home", EventType.GOALS,
                           lambda m: m.score_home == 2),
            EventCondition("home_goals_3_plus", "Home team 3+ goals", "exact_goals_home", EventType.GOALS,
                           lambda m: m.score_home >= 3),

            # --- exact_goals_away ---
            EventCondition("away_goals_0", "Away team 0 goals", "exact_goals_away", EventType.GOALS,
                           lambda m: m.score_away == 0),
            EventCondition("away_goals_1", "Away team 1 goal", "exact_goals_away", EventType.GOALS,
                           lambda m: m.score_away == 1),
            EventCondition("away_goals_2", "Away team 2 goals", "exact_goals_away", EventType.GOALS,
                           lambda m: m.score_away == 2),
            EventCondition("away_goals_3_plus", "Away team 3+ goals", "exact_goals_away", EventType.GOALS,
                           lambda m: m.score_away >= 3),

            # --- winning_margin ---
            EventCondition("win_margin_home_1", "Home win by 1 goal", "winning_margin", EventType.GOALS,
                           lambda m: m.score_home - m.score_away == 1),
            EventCondition("win_margin_home_2", "Home win by 2 goals", "winning_margin", EventType.GOALS,
                           lambda m: m.score_home - m.score_away == 2),
            EventCondition("win_margin_home_3_plus", "Home win by 3+ goals", "winning_margin", EventType.GOALS,
                           lambda m: m.score_home - m.score_away >= 3),
            EventCondition("win_margin_away_1", "Away win by 1 goal", "winning_margin", EventType.GOALS,
                           lambda m: m.score_away - m.score_home == 1),
            EventCondition("win_margin_away_2", "Away win by 2 goals", "winning_margin", EventType.GOALS,
                           lambda m: m.score_away - m.score_home == 2),
            EventCondition("win_margin_away_3_plus", "Away win by 3+ goals", "winning_margin", EventType.GOALS,
                           lambda m: m.score_away - m.score_home >= 3),
            EventCondition("win_margin_draw", "Draw", "winning_margin", EventType.GOALS,
                           lambda m: m.score_home == m.score_away),

            # --- score_both_halves ---
            EventCondition("home_score_both_halves", "Home team scores in both halves", "score_both_halves",
                           EventType.GOALS,
                           lambda m: EventPatterns._has_home_score_both_halves(m)),
            EventCondition("away_score_both_halves", "Away team scores in both halves", "score_both_halves",
                           EventType.GOALS,
                           lambda m: EventPatterns._has_away_score_both_halves(m)),

            # --- win_either_half ---
            EventCondition("home_win_either_half", "Home team wins either half", "win_either_half", EventType.GOALS,
                           lambda m: EventPatterns._home_won_either_half(m)),
            EventCondition("away_win_either_half", "Away team wins either half", "win_either_half", EventType.GOALS,
                           lambda m: EventPatterns._away_won_either_half(m)),

            # --- win_both_halves ---
            EventCondition("home_win_both_halves", "Home team wins both halves", "win_both_halves", EventType.GOALS,
                           lambda m: EventPatterns._home_won_both_halves(m)),
            EventCondition("away_win_both_halves", "Away team wins both halves", "win_both_halves", EventType.GOALS,
                           lambda m: EventPatterns._away_won_both_halves(m)),

            # --- highest_scoring_half ---
            EventCondition("highest_scoring_first", "First half highest scoring", "highest_scoring_half",
                           EventType.GOALS,
                           lambda m: EventPatterns._highest_scoring_half(m) == "first"),
            EventCondition("highest_scoring_second", "Second half highest scoring", "highest_scoring_half",
                           EventType.GOALS,
                           lambda m: EventPatterns._highest_scoring_half(m) == "second"),
            EventCondition("highest_scoring_equal", "Equal scoring halves", "highest_scoring_half", EventType.GOALS,
                           lambda m: EventPatterns._highest_scoring_half(m) == "equal"),

            # --- btts_both_halves ---
            EventCondition("btts_both_halves_yes", "Both teams score in both halves", "btts_both_halves",
                           EventType.GOALS,
                           lambda m: EventPatterns._btts_both_halves(m)),
            EventCondition("btts_both_halves_no", "Not both teams score in both halves", "btts_both_halves",
                           EventType.GOALS,
                           lambda m: not EventPatterns._btts_both_halves(m)),

            # --- no_draw_btts ---
            EventCondition("no_draw_btts_yes", "No draw & both teams score", "no_draw_btts", EventType.GOALS,
                           lambda m: m.score_home != m.score_away and m.score_home > 0 and m.score_away > 0),
            EventCondition("no_draw_btts_no", "Draw or clean sheet", "no_draw_btts", EventType.GOALS,
                           lambda m: m.score_home == m.score_away or m.score_home == 0 or m.score_away == 0),

            # --- goal_bounds ---
            EventCondition("goal_bounds_0", "Goal bounds: 0 goals", "goal_bounds", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 0),
            EventCondition("goal_bounds_0_1", "Goal bounds: 0-1 goals", "goal_bounds", EventType.GOALS,
                           lambda m: 0 <= (m.score_home + m.score_away) <= 1),
            EventCondition("goal_bounds_0_2", "Goal bounds: 0-2 goals", "goal_bounds", EventType.GOALS,
                           lambda m: 0 <= (m.score_home + m.score_away) <= 2),
            EventCondition("goal_bounds_1", "Goal bounds: 1 goal", "goal_bounds", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 1),
            EventCondition("goal_bounds_1_2", "Goal bounds: 1-2 goals", "goal_bounds", EventType.GOALS,
                           lambda m: 1 <= (m.score_home + m.score_away) <= 2),
            EventCondition("goal_bounds_1_3", "Goal bounds: 1-3 goals", "goal_bounds", EventType.GOALS,
                           lambda m: 1 <= (m.score_home + m.score_away) <= 3),
            EventCondition("goal_bounds_2", "Goal bounds: 2 goals", "goal_bounds", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 2),
            EventCondition("goal_bounds_2_3", "Goal bounds: 2-3 goals", "goal_bounds", EventType.GOALS,
                           lambda m: 2 <= (m.score_home + m.score_away) <= 3),
            EventCondition("goal_bounds_3", "Goal bounds: 3 goals", "goal_bounds", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 3),
            EventCondition("goal_bounds_3_4", "Goal bounds: 3-4 goals", "goal_bounds", EventType.GOALS,
                           lambda m: 3 <= (m.score_home + m.score_away) <= 4),
            EventCondition("goal_bounds_4", "Goal bounds: 4 goals", "goal_bounds", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 4),
            EventCondition("goal_bounds_4_5_plus", "Goal bounds: 4-5+ goals", "goal_bounds", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) >= 4),
            EventCondition("goal_bounds_5_plus", "Goal bounds: 5+ goals", "goal_bounds", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) >= 5),

            # --- excluded_goals ---
            EventCondition("excluded_goals_0", "Excluded: 0 goals", "excluded_goals", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) != 0),
            EventCondition("excluded_goals_1", "Excluded: 1 goal", "excluded_goals", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) != 1),
            EventCondition("excluded_goals_2", "Excluded: 2 goals", "excluded_goals", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) != 2),
            EventCondition("excluded_goals_3", "Excluded: 3 goals", "excluded_goals", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) != 3),
            EventCondition("excluded_goals_4", "Excluded: 4 goals", "excluded_goals", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) != 4),
            EventCondition("excluded_goals_5_plus", "Excluded: 5+ goals", "excluded_goals", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) < 5),

            # --- multigoals ---
            EventCondition("multigoals_1_2", "Multigoals: 1-2 goals", "multigoals", EventType.GOALS,
                           lambda m: 1 <= (m.score_home + m.score_away) <= 2),
            EventCondition("multigoals_1_3", "Multigoals: 1-3 goals", "multigoals", EventType.GOALS,
                           lambda m: 1 <= (m.score_home + m.score_away) <= 3),
            EventCondition("multigoals_1_4", "Multigoals: 1-4 goals", "multigoals", EventType.GOALS,
                           lambda m: 1 <= (m.score_home + m.score_away) <= 4),
            EventCondition("multigoals_2_3", "Multigoals: 2-3 goals", "multigoals", EventType.GOALS,
                           lambda m: 2 <= (m.score_home + m.score_away) <= 3),
            EventCondition("multigoals_2_4", "Multigoals: 2-4 goals", "multigoals", EventType.GOALS,
                           lambda m: 2 <= (m.score_home + m.score_away) <= 4),
            EventCondition("multigoals_3_4", "Multigoals: 3-4 goals", "multigoals", EventType.GOALS,
                           lambda m: 3 <= (m.score_home + m.score_away) <= 4),
            EventCondition("multigoals_4_5", "Multigoals: 4-5 goals", "multigoals", EventType.GOALS,
                           lambda m: 4 <= (m.score_home + m.score_away) <= 5),
            EventCondition("multigoals_5_6", "Multigoals: 5-6 goals", "multigoals", EventType.GOALS,
                           lambda m: 5 <= (m.score_home + m.score_away) <= 6),
            EventCondition("multigoals_7_plus", "Multigoals: 7+ goals", "multigoals", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) >= 7),
            EventCondition("multigoals_no_goal", "Multigoals: No goal", "multigoals", EventType.GOALS,
                           lambda m: (m.score_home + m.score_away) == 0),

            # =============================================================
            # --- MATCH RESULT MARKETS ---
            # =============================================================

            # --- 1x2 ---
            EventCondition("home_win", "Home team wins", "1x2", EventType.TEAM_STATS,
                           lambda m: m.score_home > m.score_away),
            EventCondition("draw", "Match ends in draw", "1x2", EventType.TEAM_STATS,
                           lambda m: m.score_home == m.score_away),
            EventCondition("away_win", "Away team wins", "1x2", EventType.TEAM_STATS,
                           lambda m: m.score_away > m.score_home),

            # --- double_chance ---
            EventCondition("home_or_draw", "Home win or draw", "double_chance", EventType.TEAM_STATS,
                           lambda m: m.score_home >= m.score_away),
            EventCondition("home_or_away", "Home win or away win", "double_chance", EventType.TEAM_STATS,
                           lambda m: m.score_home != m.score_away),
            EventCondition("draw_or_away", "Draw or away win", "double_chance", EventType.TEAM_STATS,
                           lambda m: m.score_home <= m.score_away),

            # --- draw_no_bet ---
            EventCondition("home_win_dnb", "Home win (draw no bet)", "draw_no_bet", EventType.TEAM_STATS,
                           lambda m: m.score_home > m.score_away),
            EventCondition("away_win_dnb", "Away win (draw no bet)", "draw_no_bet", EventType.TEAM_STATS,
                           lambda m: m.score_away > m.score_home),

            # --- halftime_fulltime ---
            EventCondition("home_home", "Home/Home (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "home_home"),
            EventCondition("home_draw", "Home/Draw (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "home_draw"),
            EventCondition("home_away", "Home/Away (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "home_away"),
            EventCondition("draw_home", "Draw/Home (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "draw_home"),
            EventCondition("draw_draw", "Draw/Draw (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "draw_draw"),
            EventCondition("draw_away", "Draw/Away (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "draw_away"),
            EventCondition("away_home", "Away/Home (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "away_home"),
            EventCondition("away_draw", "Away/Draw (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "away_draw"),
            EventCondition("away_away", "Away/Away (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
                           lambda m: EventPatterns._get_halftime_fulltime(m) == "away_away"),

            # --- home_no_bet ---
            EventCondition("home_no_bet_draw", "Home no bet: Draw", "home_no_bet", EventType.TEAM_STATS,
                           lambda m: m.score_home == m.score_away),
            EventCondition("home_no_bet_away", "Home no bet: Away", "home_no_bet", EventType.TEAM_STATS,
                           lambda m: m.score_away > m.score_home),

            # --- away_no_bet ---
            EventCondition("away_no_bet_home", "Away no bet: Home", "away_no_bet", EventType.TEAM_STATS,
                           lambda m: m.score_home > m.score_away),
            EventCondition("away_no_bet_draw", "Away no bet: Draw", "away_no_bet", EventType.TEAM_STATS,
                           lambda m: m.score_home == m.score_away),

            # =============================================================
            # --- HALF-TIME MARKETS ---
            # =============================================================

            # --- first_half_1x2 ---
            EventCondition("first_half_home_win", "First half: Home win", "first_half_1x2", EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_result(m) == "home"),
            EventCondition("first_half_draw", "First half: Draw", "first_half_1x2", EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_result(m) == "draw"),
            EventCondition("first_half_away_win", "First half: Away win", "first_half_1x2", EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_result(m) == "away"),

            # --- first_half_over_under ---
            EventCondition("first_half_over_0_5", "First half goals over 0.5", "first_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_goals(m) > 0.5),
            EventCondition("first_half_over_1_5", "First half goals over 1.5", "first_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_goals(m) > 1.5),
            EventCondition("first_half_over_2_5", "First half goals over 2.5", "first_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_goals(m) > 2.5),
            EventCondition("first_half_under_0_5", "First half goals under 0.5", "first_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_goals(m) < 0.5),
            EventCondition("first_half_under_1_5", "First half goals under 1.5", "first_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_goals(m) < 1.5),
            EventCondition("first_half_under_2_5", "First half goals under 2.5", "first_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_goals(m) < 2.5),

            # --- first_half_btts ---
            EventCondition("first_half_btts_yes", "Both teams score in first half", "first_half_btts",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_btts(m)),
            EventCondition("first_half_btts_no", "Not both teams score in first half", "first_half_btts",
                           EventType.HALF_STATS,
                           lambda m: not EventPatterns._first_half_btts(m)),

            # --- first_half_double_chance ---
            EventCondition("first_half_home_or_draw", "First half: Home or draw", "first_half_double_chance",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_result(m) in ["home", "draw"]),
            EventCondition("first_half_home_or_away", "First half: Home or away", "first_half_double_chance",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_result(m) in ["home", "away"]),
            EventCondition("first_half_draw_or_away", "First half: Draw or away", "first_half_double_chance",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._first_half_result(m) in ["draw", "away"]),

            # --- second_half_1x2 ---
            EventCondition("second_half_home_win", "Second half: Home win", "second_half_1x2", EventType.HALF_STATS,
                           lambda m: EventPatterns._second_half_result(m) == "home"),
            EventCondition("second_half_draw", "Second half: Draw", "second_half_1x2", EventType.HALF_STATS,
                           lambda m: EventPatterns._second_half_result(m) == "draw"),
            EventCondition("second_half_away_win", "Second half: Away win", "second_half_1x2", EventType.HALF_STATS,
                           lambda m: EventPatterns._second_half_result(m) == "away"),

            # --- second_half_over_under ---
            EventCondition("second_half_over_0_5", "Second half goals over 0.5", "second_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._second_half_goals(m) > 0.5),
            EventCondition("second_half_over_1_5", "Second half goals over 1.5", "second_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._second_half_goals(m) > 1.5),
            EventCondition("second_half_over_2_5", "Second half goals over 2.5", "second_half_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._second_half_goals(m) > 2.5),

            # --- second_half_btts ---
            EventCondition("second_half_btts_yes", "Both teams score in second half", "second_half_btts",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._second_half_btts(m)),
            EventCondition("second_half_btts_no", "Not both teams score in second half", "second_half_btts",
                           EventType.HALF_STATS,
                           lambda m: not EventPatterns._second_half_btts(m)),

            # --- both_halves_over_under ---
            EventCondition("both_halves_over_1_5", "Both halves over 1.5 goals", "both_halves_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._both_halves_over_1_5(m)),
            EventCondition("both_halves_under_1_5", "Both halves under 1.5 goals", "both_halves_over_under",
                           EventType.HALF_STATS,
                           lambda m: EventPatterns._both_halves_under_1_5(m)),

            # --- 1st_2nd_half_gg_ng ---
            EventCondition("half_gg_ng_no_no", "Half GG/NG: No/No", "1st_2nd_half_gg_ng", EventType.HALF_STATS,
                           lambda m: EventPatterns._half_gg_ng(m) == "no_no"),
            EventCondition("half_gg_ng_yes_no", "Half GG/NG: Yes/No", "1st_2nd_half_gg_ng", EventType.HALF_STATS,
                           lambda m: EventPatterns._half_gg_ng(m) == "yes_no"),
            EventCondition("half_gg_ng_yes_yes", "Half GG/NG: Yes/Yes", "1st_2nd_half_gg_ng", EventType.HALF_STATS,
                           lambda m: EventPatterns._half_gg_ng(m) == "yes_yes"),
            EventCondition("half_gg_ng_no_yes", "Half GG/NG: No/Yes", "1st_2nd_half_gg_ng", EventType.HALF_STATS,
                           lambda m: EventPatterns._half_gg_ng(m) == "no_yes"),

            # =============================================================
            # --- SHOTS MARKETS ---
            # =============================================================

            # Total Shots
            EventCondition("total_shots_over_25_5", "Total shots over 25.5", "total_shots_over_under",
                           EventType.SHOTS,
                           lambda m: EventPatterns._total_shots(m) > 25.5),
            EventCondition("total_shots_under_25_5", "Total shots under 25.5", "total_shots_over_under",
                           EventType.SHOTS,
                           lambda m: EventPatterns._total_shots(m) < 25.5),

            # Home Team Total Shots
            EventCondition("home_shots_over_12_5", "Home team shots over 12.5", "team_shots_home", EventType.SHOTS,
                           lambda m: EventPatterns._home_shots(m) > 12.5),
            EventCondition("home_shots_over_14_5", "Home team shots over 14.5", "team_shots_home", EventType.SHOTS,
                           lambda m: EventPatterns._home_shots(m) > 14.5),

            # Away Team Total Shots
            EventCondition("away_shots_over_11_5", "Away team shots over 11.5", "team_shots_away", EventType.SHOTS,
                           lambda m: EventPatterns._away_shots(m) > 11.5),
            EventCondition("away_shots_over_13_5", "Away team shots over 13.5", "team_shots_away", EventType.SHOTS,
                           lambda m: EventPatterns._away_shots(m) > 13.5),

            # Shots On Target
            EventCondition("shots_on_target_over_8_5", "Shots on target over 8.5", "shots_on_target_over_under",
                           EventType.SHOT_ON_TARGET,
                           lambda m: EventPatterns._total_shots_on_target(m) > 8.5),
            EventCondition("shots_on_target_under_8_5", "Shots on target under 8.5", "shots_on_target_over_under",
                           EventType.SHOT_ON_TARGET,
                           lambda m: EventPatterns._total_shots_on_target(m) < 8.5),

            # Home Team Shots On Target
            EventCondition("home_shots_on_target_over_4_5", "Home team shots on target over 4.5",
                           "team_shots_on_target_home", EventType.SHOT_ON_TARGET,
                           lambda m: EventPatterns._home_shots_on_target(m) > 4.5),
            EventCondition("home_shots_on_target_under_4_5", "Home team shots on target under 4.5",
                           "team_shots_on_target_home", EventType.SHOT_ON_TARGET,
                           lambda m: EventPatterns._home_shots_on_target(m) < 4.5),

            # Away Team Shots On Target
            EventCondition("away_shots_on_target_over_4_5", "Away team shots on target over 4.5",
                           "team_shots_on_target_away", EventType.SHOT_ON_TARGET,
                           lambda m: EventPatterns._away_shots_on_target(m) > 4.5),
            EventCondition("away_shots_on_target_under_4_5", "Away team shots on target under 4.5",
                           "team_shots_on_target_away", EventType.SHOT_ON_TARGET,
                           lambda m: EventPatterns._away_shots_on_target(m) < 4.5),

            # First Shot on Target
            EventCondition("first_shot_on_target_home", "First shot on target by home team", "first_shot_on_target",
                           EventType.SHOT_ON_TARGET,
                           lambda m: EventPatterns._first_shot_on_target(m) == "home"),
            EventCondition("first_shot_on_target_away", "First shot on target by away team", "first_shot_on_target",
                           EventType.SHOT_ON_TARGET,
                           lambda m: EventPatterns._first_shot_on_target(m) == "away"),

            # =============================================================
            # --- PENALTY MARKETS ---
            # =============================================================

            EventCondition("penalty_awarded_yes", "Penalty awarded in match", "penalty_awarded",
                           EventType.PENALTY_AWARDED,
                           lambda m: EventPatterns._penalty_awarded(m)),
            EventCondition("penalty_awarded_no", "No penalty awarded in match", "penalty_awarded",
                           EventType.PENALTY_AWARDED,
                           lambda m: not EventPatterns._penalty_awarded(m)),

            EventCondition("home_penalty_awarded_yes", "Home team penalty awarded", "team_penalty_awarded_home",
                           EventType.PENALTY_AWARDED,
                           lambda m: EventPatterns._home_penalty_awarded(m)),
            EventCondition("away_penalty_awarded_yes", "Away team penalty awarded", "team_penalty_awarded_away",
                           EventType.PENALTY_AWARDED,
                           lambda m: EventPatterns._away_penalty_awarded(m)),

            EventCondition("two_penalties_awarded_yes", "Two penalties awarded in match", "two_penalties_awarded",
                           EventType.PENALTY_AWARDED,
                           lambda m: EventPatterns._two_penalties_awarded(m)),

            EventCondition("penalty_first_half_yes", "Penalty awarded in first half", "penalty_first_half",
                           EventType.PENALTY_AWARDED,
                           lambda m: EventPatterns._penalty_first_half(m)),

            # =============================================================
            # --- METHOD OF GOAL SCORING ---
            # =============================================================

            EventCondition("goal_method_shot", "First goal scored by shot", "goal_method", EventType.GOALS,
                           lambda m: EventPatterns._first_goal_method(m) == "shot"),
            EventCondition("goal_method_header", "First goal scored by header", "goal_method", EventType.GOALS,
                           lambda m: EventPatterns._first_goal_method(m) == "header"),
            EventCondition("goal_method_penalty", "First goal scored by penalty", "goal_method", EventType.GOALS,
                           lambda m: EventPatterns._first_goal_method(m) == "penalty"),
            EventCondition("goal_method_own_goal", "First goal is own goal", "goal_method", EventType.GOALS,
                           lambda m: EventPatterns._first_goal_method(m) == "own_goal"),
            EventCondition("goal_method_free_kick", "First goal scored by free kick", "goal_method", EventType.GOALS,
                           lambda m: EventPatterns._first_goal_method(m) == "free_kick"),

            # =============================================================
            # --- FIRST EVENT MARKETS ---
            # =============================================================

            EventCondition("first_event_throw_in", "First event is throw-in", "first_event", EventType.THROW_IN,
                           lambda m: EventPatterns._first_event(m) == "throw_in"),
            EventCondition("first_event_free_kick", "First event is free kick", "first_event", EventType.FREE_KICK,
                           lambda m: EventPatterns._first_event(m) == "free_kick"),
            EventCondition("first_event_goal_kick", "First event is goal kick", "first_event", EventType.GOAL_KICK,
                           lambda m: EventPatterns._first_event(m) == "goal_kick"),
            EventCondition("first_event_corner", "First event is corner", "first_event", EventType.CORNER,
                           lambda m: EventPatterns._first_event(m) == "corner"),
            EventCondition("first_event_goal", "First event is goal", "first_event", EventType.GOALS,
                           lambda m: EventPatterns._first_event(m) == "goal"),

            # =============================================================
            # --- OWN GOAL MARKETS ---
            # =============================================================

            EventCondition("own_goal_yes", "Own goal scored in match", "own_goal", EventType.GOALS,
                           lambda m: EventPatterns._own_goal_scored(m)),

            # =============================================================
            # --- TIME OF FIRST GOAL ---
            # =============================================================

            EventCondition("first_goal_before_28", "First goal before 28 minutes", "first_goal_time", EventType.GOALS,
                           lambda m: EventPatterns._first_goal_minute(m) < 28),
            EventCondition("first_goal_after_28", "First goal after 28 minutes", "first_goal_time", EventType.GOALS,
                           lambda m: EventPatterns._first_goal_minute(m) >= 28),

            # =============================================================
            # --- CARDS MARKETS ---
            # =============================================================

            # --- total_cards_over_under ---
            EventCondition("over_0_5_cards", "Total cards over 0.5", "total_cards_over_under", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) > 0.5),
            EventCondition("over_1_5_cards", "Total cards over 1.5", "total_cards_over_under", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) > 1.5),
            EventCondition("over_2_5_cards", "Total cards over 2.5", "total_cards_over_under", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) > 2.5),
            EventCondition("over_3_5_cards", "Total cards over 3.5", "total_cards_over_under", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) > 3.5),
            EventCondition("under_3_5_cards", "Total cards under 3.5", "total_cards_over_under", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) < 3.5),
            EventCondition("over_4_5_cards", "Total cards over 4.5", "total_cards_over_under", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) > 4.5),
            EventCondition("over_5_5_cards", "Total cards over 5.5", "total_cards_over_under", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) > 5.5),

            # --- team_cards_over_under ---
            EventCondition("home_over_0_5_cards", "Home team cards over 0.5", "team_cards_home", EventType.CARDS,
                           lambda m: EventPatterns._home_cards(m) > 0.5),
            EventCondition("home_over_1_5_cards", "Home team cards over 1.5", "team_cards_home", EventType.CARDS,
                           lambda m: EventPatterns._home_cards(m) > 1.5),
            EventCondition("home_over_2_5_cards", "Home team cards over 2.5", "team_cards_home", EventType.CARDS,
                           lambda m: EventPatterns._home_cards(m) > 2.5),
            EventCondition("away_over_0_5_cards", "Away team cards over 0.5", "team_cards_away", EventType.CARDS,
                           lambda m: EventPatterns._away_cards(m) > 0.5),
            EventCondition("away_over_1_5_cards", "Away team cards over 1.5", "team_cards_away", EventType.CARDS,
                           lambda m: EventPatterns._away_cards(m) > 1.5),
            EventCondition("away_over_2_5_cards", "Away team cards over 2.5", "team_cards_away", EventType.CARDS,
                           lambda m: EventPatterns._away_cards(m) > 2.5),

            # --- first_half_cards_over_under ---
            EventCondition("first_half_over_0_5_cards", "First half cards over 0.5", "first_half_cards",
                           EventType.CARDS,
                           lambda m: EventPatterns._first_half_cards(m) > 0.5),
            EventCondition("first_half_over_1_5_cards", "First half cards over 1.5", "first_half_cards",
                           EventType.CARDS,
                           lambda m: EventPatterns._first_half_cards(m) > 1.5),
            EventCondition("first_half_over_2_5_cards", "First half cards over 2.5", "first_half_cards",
                           EventType.CARDS,
                           lambda m: EventPatterns._first_half_cards(m) > 2.5),

            # --- second_half_cards_over_under ---
            EventCondition("second_half_over_1_5_cards", "Second half cards over 1.5", "second_half_cards",
                           EventType.CARDS,
                           lambda m: EventPatterns._second_half_cards(m) > 1.5),
            EventCondition("second_half_over_2_5_cards", "Second half cards over 2.5", "second_half_cards",
                           EventType.CARDS,
                           lambda m: EventPatterns._second_half_cards(m) > 2.5),
            EventCondition("second_half_over_3_5_cards", "Second half cards over 3.5", "second_half_cards",
                           EventType.CARDS,
                           lambda m: EventPatterns._second_half_cards(m) > 3.5),

            # --- match_cards ---
            EventCondition("match_cards_4_plus", "Match cards 4+", "match_cards", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) >= 4),
            EventCondition("match_cards_5_plus", "Match cards 5+", "match_cards", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) >= 5),
            EventCondition("match_cards_6_plus", "Match cards 6+", "match_cards", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) >= 6),
            EventCondition("match_cards_7_plus", "Match cards 7+", "match_cards", EventType.CARDS,
                           lambda m: EventPatterns._total_cards(m) >= 7),

            # --- total_red_cards_over_under ---
            EventCondition("over_0_5_red_cards", "Total red cards over 0.5", "total_red_cards_over_under",
                           EventType.RED_CARD,
                           lambda m: EventPatterns._total_red_cards(m) > 0.5),
            EventCondition("over_1_5_red_cards", "Total red cards over 1.5", "total_red_cards_over_under",
                           EventType.RED_CARD,
                           lambda m: EventPatterns._total_red_cards(m) > 1.5),
            EventCondition("under_0_5_red_cards", "Total red cards under 0.5", "total_red_cards_over_under",
                           EventType.RED_CARD,
                           lambda m: EventPatterns._total_red_cards(m) < 0.5),
            EventCondition("under_1_5_red_cards", "Total red cards under 1.5", "total_red_cards_over_under",
                           EventType.RED_CARD,
                           lambda m: EventPatterns._total_red_cards(m) < 1.5),

            # --- both_teams_receive_card ---
            EventCondition("both_teams_card_yes", "Both teams receive a card", "both_teams_receive_card",
                           EventType.CARDS,
                           lambda m: EventPatterns._both_teams_receive_card(m)),
            EventCondition("both_teams_card_no", "Not both teams receive a card", "both_teams_receive_card",
                           EventType.CARDS,
                           lambda m: not EventPatterns._both_teams_receive_card(m)),

            # --- card_shown_both_halves ---
            EventCondition("card_both_halves_yes", "Card shown in both halves", "card_shown_both_halves",
                           EventType.CARDS,
                           lambda m: EventPatterns._card_shown_both_halves(m)),
            EventCondition("card_both_halves_no", "No card shown in both halves", "card_shown_both_halves",
                           EventType.CARDS,
                           lambda m: not EventPatterns._card_shown_both_halves(m)),

            # --- first_card_before_35 ---
            EventCondition("first_card_before_35_yes", "First card before 35:00", "first_card_before_35",
                           EventType.CARDS,
                           lambda m: EventPatterns._first_card_minute(m) < 35),
            EventCondition("first_card_before_35_no", "No first card before 35:00", "first_card_before_35",
                           EventType.CARDS,
                           lambda m: EventPatterns._first_card_minute(m) >= 35),

            # --- red_card_first_half ---
            EventCondition("red_card_first_half_yes", "Red card in first half", "red_card_first_half",
                           EventType.RED_CARD,
                           lambda m: EventPatterns._red_card_first_half(m)),
            EventCondition("red_card_first_half_no", "No red card in first half", "red_card_first_half",
                           EventType.RED_CARD,
                           lambda m: not EventPatterns._red_card_first_half(m)),

            # --- straight_red_card ---
            EventCondition("straight_red_card_yes", "Straight red card in match", "straight_red_card",
                           EventType.RED_CARD,
                           lambda m: EventPatterns._straight_red_card(m)),
            EventCondition("straight_red_card_no", "No straight red card in match", "straight_red_card",
                           EventType.RED_CARD,
                           lambda m: not EventPatterns._straight_red_card(m)),

            # --- yellow_card_markets ---
            EventCondition("yellow_card_yes", "Yellow card shown", "yellow_card", EventType.YELLOW_CARD,
                           lambda m: EventPatterns._total_yellow_cards(m) > 0),
            EventCondition("yellow_card_no", "No yellow card shown", "yellow_card", EventType.YELLOW_CARD,
                           lambda m: EventPatterns._total_yellow_cards(m) == 0),

            EventCondition("home_yellow_card_yes", "Home team yellow card", "team_yellow_card_home",
                           EventType.YELLOW_CARD,
                           lambda m: EventPatterns._home_yellow_cards(m) > 0),
            EventCondition("away_yellow_card_yes", "Away team yellow card", "team_yellow_card_away",
                           EventType.YELLOW_CARD,
                           lambda m: EventPatterns._away_yellow_cards(m) > 0),

            # --- second_yellow_card ---
            EventCondition("second_yellow_yes", "Second yellow card shown", "second_yellow_card",
                           EventType.SECOND_YELLOW,
                           lambda m: EventPatterns._second_yellow_cards(m) > 0),
            EventCondition("second_yellow_no", "No second yellow card", "second_yellow_card", EventType.SECOND_YELLOW,
                           lambda m: EventPatterns._second_yellow_cards(m) == 0),

            # --- red_card_or_penalty ---
            EventCondition("red_card_or_penalty_yes", "Red card or penalty awarded", "red_card_or_penalty",
                           EventType.CARDS,
                           lambda m: EventPatterns._red_card_or_penalty(m)),
            EventCondition("red_card_or_penalty_no", "No red card or penalty", "red_card_or_penalty", EventType.CARDS,
                           lambda m: not EventPatterns._red_card_or_penalty(m)),

            # --- red_card_and_penalty ---
            EventCondition("red_card_and_penalty_yes", "Red card and penalty awarded", "red_card_and_penalty",
                           EventType.CARDS,
                           lambda m: EventPatterns._red_card_and_penalty(m)),
            EventCondition("red_card_and_penalty_no", "No red card and penalty", "red_card_and_penalty",
                           EventType.CARDS,
                           lambda m: not EventPatterns._red_card_and_penalty(m)),

            # =============================================================
            # --- TIME-BASED GOAL MARKETS ---
            # =============================================================

            # --- first_goal_before_29 ---
            EventCondition("first_goal_before_29_yes", "First goal before 29:00", "first_goal_before_29",
                           EventType.GOALS,
                           lambda m: EventPatterns._first_goal_minute(m) < 29),
            EventCondition("first_goal_before_29_no", "No first goal before 29:00", "first_goal_before_29",
                           EventType.GOALS,
                           lambda m: EventPatterns._first_goal_minute(m) >= 29),

            # --- goal_after_70 ---
            EventCondition("goal_after_70_yes", "Goal scored after 70:00", "goal_after_70", EventType.GOALS,
                           lambda m: EventPatterns._any_goal_after_minute(m, 70)),
            EventCondition("goal_after_70_no", "No goal after 70:00", "goal_after_70", EventType.GOALS,
                           lambda m: not EventPatterns._any_goal_after_minute(m, 70)),

            # --- time_first_goal_over_under ---
            EventCondition("first_goal_over_28", "Time of first goal over 28:00", "time_first_goal_over_under",
                           EventType.GOALS,
                           lambda m: EventPatterns._first_goal_minute(m) > 28),
            EventCondition("first_goal_under_28", "Time of first goal under 27:59", "time_first_goal_over_under",
                           EventType.GOALS,
                           lambda m: 0 < EventPatterns._first_goal_minute(m) <= 28),
            EventCondition("first_goal_no_score", "No score in match", "time_first_goal_over_under", EventType.GOALS,
                           lambda m: EventPatterns._first_goal_minute(m) == 0),

            # =============================================================
            # --- CORNERS MARKETS ---
            # =============================================================

            # Corners 3-Way
            EventCondition("corners_3way_home", "Home team wins most corners", "corners_3way", EventType.CORNER,
                           lambda m: EventPatterns._home_corners(m) > EventPatterns._away_corners(m)),
            EventCondition("corners_3way_away", "Away team wins most corners", "corners_3way", EventType.CORNER,
                           lambda m: EventPatterns._away_corners(m) > EventPatterns._home_corners(m)),
            EventCondition("corners_3way_draw", "Equal number of corners", "corners_3way", EventType.CORNER,
                           lambda m: EventPatterns._home_corners(m) == EventPatterns._away_corners(m)),

            # Corner Ranges
            EventCondition("corner_range_0_8", "Corner range 0-8", "corner_range", EventType.CORNER,
                           lambda m: 0 <= EventPatterns._total_corners(m) <= 8),
            EventCondition("corner_range_9_11", "Corner range 9-11", "corner_range", EventType.CORNER,
                           lambda m: 9 <= EventPatterns._total_corners(m) <= 11),
            EventCondition("corner_range_12_plus", "Corner range 12+", "corner_range", EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) >= 12),

            # Next Corner Team
            EventCondition("next_corner_home", "Next corner by home team", "next_corner", EventType.CORNER,
                           lambda m: EventPatterns._next_corner_team(m) == "home"),
            EventCondition("next_corner_away", "Next corner by away team", "next_corner", EventType.CORNER,
                           lambda m: EventPatterns._next_corner_team(m) == "away"),

            # Team With Most Corners
            EventCondition("most_corners_home", "Home team has most corners", "most_corners", EventType.CORNER,
                           lambda m: EventPatterns._home_corners(m) > EventPatterns._away_corners(m)),
            EventCondition("most_corners_away", "Away team has most corners", "most_corners", EventType.CORNER,
                           lambda m: EventPatterns._away_corners(m) > EventPatterns._home_corners(m)),

            # Half With Most Corners
            EventCondition("most_corners_first_half", "First half has most corners", "half_most_corners",
                           EventType.CORNER,
                           lambda m: EventPatterns._first_half_corners(m) > EventPatterns._second_half_corners(m)),
            EventCondition("most_corners_second_half", "Second half has most corners", "half_most_corners",
                           EventType.CORNER,
                           lambda m: EventPatterns._second_half_corners(m) > EventPatterns._first_half_corners(m)),

            # Corners Odd/Even
            EventCondition("corners_odd", "Total corners odd", "corners_odd_even", EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) % 2 == 1),
            EventCondition("corners_even", "Total corners even", "corners_odd_even", EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) % 2 == 0),

            # --- total_corners_over_under ---
            EventCondition("over_8_5_corners", "Total corners over 8.5", "total_corners_over_under", EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) > 8.5),
            EventCondition("over_9_5_corners", "Total corners over 9.5", "total_corners_over_under", EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) > 9.5),
            EventCondition("over_10_5_corners", "Total corners over 10.5", "total_corners_over_under",
                           EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) > 10.5),

            # --- team_corners_over_under ---
            EventCondition("home_over_4_5_corners", "Home team corners over 4.5", "team_corners_home",
                           EventType.CORNER,
                           lambda m: EventPatterns._home_corners(m) > 4.5),
            EventCondition("home_over_5_5_corners", "Home team corners over 5.5", "team_corners_home",
                           EventType.CORNER,
                           lambda m: EventPatterns._home_corners(m) > 5.5),
            EventCondition("away_over_1_5_corners", "Away team corners over 1.5", "team_corners_away",
                           EventType.CORNER,
                           lambda m: EventPatterns._away_corners(m) > 1.5),
            EventCondition("away_over_2_5_corners", "Away team corners over 2.5", "team_corners_away",
                           EventType.CORNER,
                           lambda m: EventPatterns._away_corners(m) > 2.5),

            # --- first_half_corners_over_under ---
            EventCondition("first_half_over_3_5_corners", "First half corners over 3.5", "first_half_corners",
                           EventType.CORNER,
                           lambda m: EventPatterns._first_half_corners(m) > 3.5),
            EventCondition("first_half_over_4_5_corners", "First half corners over 4.5", "first_half_corners",
                           EventType.CORNER,
                           lambda m: EventPatterns._first_half_corners(m) > 4.5),
            EventCondition("first_half_over_5_5_corners", "First half corners over 5.5", "first_half_corners",
                           EventType.CORNER,
                           lambda m: EventPatterns._first_half_corners(m) > 5.5),

            # --- corner_range ---
            EventCondition("corner_range_0_8", "Corner range 0-8", "corner_range", EventType.CORNER,
                           lambda m: 0 <= EventPatterns._total_corners(m) <= 8),
            EventCondition("corner_range_9_11", "Corner range 9-11", "corner_range", EventType.CORNER,
                           lambda m: 9 <= EventPatterns._total_corners(m) <= 11),
            EventCondition("corner_range_12_plus", "Corner range 12+", "corner_range", EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) >= 12),

            # --- odd_even_corners ---
            EventCondition("corners_odd", "Total corners odd", "odd_even_corners", EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) % 2 == 1),
            EventCondition("corners_even", "Total corners even", "odd_even_corners", EventType.CORNER,
                           lambda m: EventPatterns._total_corners(m) % 2 == 0),
        ]

    # Real data methods - these should use actual API data

    # In your EventPatterns class, update the helper methods:

    @staticmethod
    def _total_cards(match: Match) -> int:
        """Get total cards from match data - red cards count as 2 cards"""
        home_yellow = match.home_stats.yellow_cards if match.home_stats else 0
        home_red = match.home_stats.red_cards if match.home_stats else 0
        away_yellow = match.away_stats.yellow_cards if match.away_stats else 0
        away_red = match.away_stats.red_cards if match.away_stats else 0

        # Red cards count as 2 cards each
        return home_yellow + (home_red * 2) + away_yellow + (away_red * 2)

    @staticmethod
    def _home_cards(match: Match) -> int:
        """Get home team cards from match data - red cards count as 2 cards"""
        yellow = match.home_stats.yellow_cards if match.home_stats else 0
        red = match.home_stats.red_cards if match.home_stats else 0
        return yellow + (red * 2)

    @staticmethod
    def _away_cards(match: Match) -> int:
        """Get away team cards from match data - red cards count as 2 cards"""
        yellow = match.away_stats.yellow_cards if match.away_stats else 0
        red = match.away_stats.red_cards if match.away_stats else 0
        return yellow + (red * 2)

    @staticmethod
    def _first_half_cards(match: Match) -> int:
        """Get first half cards from match data - red cards count as 2 cards"""
        home_yellow = match.first_half.home_yellow_cards if hasattr(match.first_half, 'home_yellow_cards') else 0
        home_red = match.first_half.home_red_cards if hasattr(match.first_half, 'home_red_cards') else 0
        away_yellow = match.first_half.away_yellow_cards if hasattr(match.first_half, 'away_yellow_cards') else 0
        away_red = match.first_half.away_red_cards if hasattr(match.first_half, 'away_red_cards') else 0

        return home_yellow + (home_red * 2) + away_yellow + (away_red * 2)

    @staticmethod
    def _second_half_cards(match: Match) -> int:
        """Get second half cards from match data - red cards count as 2 cards"""
        home_yellow = match.second_half.home_yellow_cards if hasattr(match.second_half, 'home_yellow_cards') else 0
        home_red = match.second_half.home_red_cards if hasattr(match.second_half, 'home_red_cards') else 0
        away_yellow = match.second_half.away_yellow_cards if hasattr(match.second_half, 'away_yellow_cards') else 0
        away_red = match.second_half.away_red_cards if hasattr(match.second_half, 'away_red_cards') else 0

        return home_yellow + (home_red * 2) + away_yellow + (away_red * 2)

    @staticmethod
    def _total_yellow_cards(match: Match) -> int:
        """Get total yellow cards from match data (red cards NOT included)"""
        home_yellow = match.home_stats.yellow_cards if match.home_stats else 0
        away_yellow = match.away_stats.yellow_cards if match.away_stats else 0
        return home_yellow + away_yellow

    @staticmethod
    def _home_yellow_cards(match: Match) -> int:
        """Get home team yellow cards from match data (red cards NOT included)"""
        return match.home_stats.yellow_cards if match.home_stats else 0

    @staticmethod
    def _away_yellow_cards(match: Match) -> int:
        """Get away team yellow cards from match data (red cards NOT included)"""
        return match.away_stats.yellow_cards if match.away_stats else 0

    @staticmethod
    def _total_red_cards(match: Match) -> int:
        """Get total red cards from match data (counted as individual red cards)"""
        home_red = match.home_stats.red_cards if match.home_stats else 0
        away_red = match.away_stats.red_cards if match.away_stats else 0
        return home_red + away_red

    @staticmethod
    def _both_teams_receive_card(match: Match) -> bool:
        """Check if both teams received at least one card (any type)"""
        home_cards = EventPatterns._home_cards(match)
        away_cards = EventPatterns._away_cards(match)
        return home_cards > 0 and away_cards > 0

    @staticmethod
    def _card_shown_both_halves(match: Match) -> bool:
        """Check if card was shown in both halves (any type)"""
        first_half_cards = EventPatterns._first_half_cards(match)
        second_half_cards = EventPatterns._second_half_cards(match)
        return first_half_cards > 0 and second_half_cards > 0

    # Add these helper methods if they don't exist in your HalfStats class
    @staticmethod
    def _get_first_half_yellow_cards(match: Match) -> Tuple[int, int]:
        """Get first half yellow cards for home and away teams"""
        # If your HalfStats doesn't have yellow/red card breakdown, estimate from events
        home_yellow = 0
        away_yellow = 0
        for event in match.events:
            if (event.event_type in [EventType.YELLOW_CARD, EventType.SECOND_YELLOW] and
                    event.minute and event.minute <= 45):
                if event.is_home:
                    home_yellow += 1
                else:
                    away_yellow += 1
        return home_yellow, away_yellow

    @staticmethod
    def _get_first_half_red_cards(match: Match) -> Tuple[int, int]:
        """Get first half red cards for home and away teams"""
        home_red = 0
        away_red = 0
        for event in match.events:
            if (event.event_type in [EventType.RED_CARD, EventType.SECOND_YELLOW] and
                    event.minute and event.minute <= 45):
                if event.is_home:
                    home_red += 1
                else:
                    away_red += 1
        return home_red, away_red

    @staticmethod
    def _get_second_half_yellow_cards(match: Match) -> Tuple[int, int]:
        """Get second half yellow cards for home and away teams"""
        home_yellow = 0
        away_yellow = 0
        for event in match.events:
            if (event.event_type in [EventType.YELLOW_CARD, EventType.SECOND_YELLOW] and
                    event.minute and event.minute > 45):
                if event.is_home:
                    home_yellow += 1
                else:
                    away_yellow += 1
        return home_yellow, away_yellow

    @staticmethod
    def _get_second_half_red_cards(match: Match) -> Tuple[int, int]:
        """Get second half red cards for home and away teams"""
        home_red = 0
        away_red = 0
        for event in match.events:
            if (event.event_type in [EventType.RED_CARD, EventType.SECOND_YELLOW] and
                    event.minute and event.minute > 45):
                if event.is_home:
                    home_red += 1
                else:
                    away_red += 1
        return home_red, away_red

    @staticmethod
    def _second_yellow_cards(match: Match) -> int:
        """Get count of second yellow cards (red cards from second yellows)"""
        second_yellow_count = 0
        for event in match.events:
            if (event.event_type == EventType.SECOND_YELLOW or
                    (event.event_type == EventType.RED_CARD and "second yellow" in event.description.lower())):
                second_yellow_count += 1
        return second_yellow_count

    @staticmethod
    def _first_card_minute(match: Match) -> int:
        """Get minute of first card in match"""
        first_card_minute = 999
        for event in match.events:
            if (event.event_type in [EventType.YELLOW_CARD, EventType.RED_CARD, EventType.SECOND_YELLOW] and
                    event.minute and event.minute > 0):
                first_card_minute = min(first_card_minute, event.minute)
        return first_card_minute if first_card_minute != 999 else 0

    @staticmethod
    def _red_card_first_half(match: Match) -> bool:
        """Check if red card was shown in first half"""
        for event in match.events:
            if (event.event_type in [EventType.RED_CARD, EventType.SECOND_YELLOW] and
                    event.minute and event.minute <= 45):
                return True
        return False

    @staticmethod
    def _straight_red_card(match: Match) -> bool:
        """Check if straight red card was shown (not second yellow)"""
        for event in match.events:
            if (event.event_type == EventType.RED_CARD and
                    "second yellow" not in event.description.lower()):
                return True
        return False

    @staticmethod
    def _red_card_or_penalty(match: Match) -> bool:
        """Check if red card OR penalty was awarded"""
        return EventPatterns._total_red_cards(match) > 0 or EventPatterns._penalty_awarded(match)

    @staticmethod
    def _red_card_and_penalty(match: Match) -> bool:
        """Check if red card AND penalty were both awarded"""
        return EventPatterns._total_red_cards(match) > 0 and EventPatterns._penalty_awarded(match)

    @staticmethod
    def _first_shot_on_target(match: Match) -> str:
        """Determine which team had first shot on target"""
        first_shot_minute = 999
        first_shot_team = None

        for event in match.events:
            if (event.event_type == EventType.SHOT_ON_TARGET and
                    event.minute and 0 < event.minute < first_shot_minute):
                first_shot_minute = event.minute
                first_shot_team = event.team

        if first_shot_team:
            return "home" if first_shot_team == match.home_team else "away"

        # Fallback: check shots on target stats and assume home team had first if they have more
        home_sot = EventPatterns._home_shots_on_target(match)
        away_sot = EventPatterns._away_shots_on_target(match)
        return "home" if home_sot >= away_sot else "away"

    @staticmethod
    def _home_penalty_awarded(match: Match) -> bool:
        """Check if home team was awarded penalty"""
        for event in match.events:
            if (event.event_type == EventType.GOALS and
                    "penalty" in event.description.lower() and
                    event.team == match.home_team):
                return True

        # Alternative: check penalty events directly
        for event in match.events:
            if (event.event_type == EventType.PENALTY_AWARDED and
                    event.team == match.home_team):
                return True
        return False

    @staticmethod
    def _away_penalty_awarded(match: Match) -> bool:
        """Check if away team was awarded penalty"""
        for event in match.events:
            if (event.event_type == EventType.GOALS and
                    "penalty" in event.description.lower() and
                    event.team == match.away_team):
                return True

        # Alternative: check penalty events directly
        for event in match.events:
            if (event.event_type == EventType.PENALTY_AWARDED and
                    event.team == match.away_team):
                return True
        return False

    @staticmethod
    def _first_goal_method(match: Match) -> str:
        """Get method of first goal"""
        first_goal_minute = 999
        first_goal_event = None

        for event in match.events:
            if event.event_type == EventType.GOALS and event.minute and event.minute > 0:
                if event.minute < first_goal_minute:
                    first_goal_minute = event.minute
                    first_goal_event = event

        if not first_goal_event:
            return "shot"  # Default if no goal

        description = first_goal_event.description.lower()

        if "penalty" in description:
            return "penalty"
        elif "header" in description or "headed" in description:
            return "header"
        elif "own goal" in description:
            return "own_goal"
        elif "free kick" in description:
            return "free_kick"
        else:
            return "shot"

    @staticmethod
    def _first_event(match: Match) -> str:
        """Get first event type in match"""
        if not match.events:
            return "throw_in"  # Default

        first_event = min(match.events, key=lambda x: x.minute if x.minute else 999)

        if first_event.event_type == EventType.THROW_IN:
            return "throw_in"
        elif first_event.event_type == EventType.FREE_KICK:
            return "free_kick"
        elif first_event.event_type == EventType.GOAL_KICK:
            return "goal_kick"
        elif first_event.event_type == EventType.CORNER:
            return "corner"
        elif first_event.event_type == EventType.GOALS:
            return "goal"
        else:
            return "throw_in"  # Default

    @staticmethod
    def _next_corner_team(match: Match) -> str:
        """Determine which team gets next corner (predictive)"""
        # This is a predictive market - use historical pattern or recent corner frequency
        home_corners = EventPatterns._home_corners(match)
        away_corners = EventPatterns._away_corners(match)

        # Simple heuristic: team with fewer corners is more likely to get next one
        if away_corners < home_corners:
            return "away"
        else:
            return "home"

    @staticmethod
    def _total_shots(match: Match) -> int:
        """Get total shots from match data"""
        home_shots = match.home_stats.total_shots if match.home_stats else 0
        away_shots = match.away_stats.total_shots if match.away_stats else 0
        return home_shots + away_shots

    @staticmethod
    def _home_shots(match: Match) -> int:
        """Get home team shots from match data"""
        return match.home_stats.total_shots if match.home_stats else 0

    @staticmethod
    def _away_shots(match: Match) -> int:
        """Get away team shots from match data"""
        return match.away_stats.total_shots if match.away_stats else 0

    @staticmethod
    def _total_shots_on_target(match: Match) -> int:
        """Get total shots on target from match data"""
        home_sot = match.home_stats.shots_on_goal if match.home_stats else 0
        away_sot = match.away_stats.shots_on_goal if match.away_stats else 0
        return home_sot + away_sot

    @staticmethod
    def _home_shots_on_target(match: Match) -> int:
        """Get home team shots on target from match data"""
        return match.home_stats.shots_on_goal if match.home_stats else 0

    @staticmethod
    def _away_shots_on_target(match: Match) -> int:
        """Get away team shots on target from match data"""
        return match.away_stats.shots_on_goal if match.away_stats else 0

    @staticmethod
    def _penalty_awarded(match: Match) -> bool:
        """Check if penalty was awarded in match"""
        # Check events for penalty awards
        for event in match.events:
            if event.event_type == EventType.GOALS and "penalty" in event.description.lower():
                return True
        return False

    @staticmethod
    def _two_penalties_awarded(match: Match) -> bool:
        """Check if two penalties were awarded"""
        penalty_count = 0
        for event in match.events:
            if event.event_type == EventType.GOALS and "penalty" in event.description.lower():
                penalty_count += 1
        return penalty_count >= 2

    @staticmethod
    def _penalty_first_half(match: Match) -> bool:
        """Check if penalty was awarded in first half"""
        for event in match.events:
            if (event.event_type == EventType.GOALS and "penalty" in event.description.lower()
                    and event.minute and event.minute <= 45):
                return True
        return False

    @staticmethod
    def _own_goal_scored(match: Match) -> bool:
        """Check if own goal was scored"""
        for event in match.events:
            if event.event_type == EventType.GOALS and "own goal" in event.description.lower():
                return True
        return False

    @staticmethod
    def _first_goal_minute(match: Match) -> int:
        """Get minute of first goal"""
        first_goal_minute = 999
        for event in match.events:
            if event.event_type == EventType.GOALS and event.minute:
                first_goal_minute = min(first_goal_minute, event.minute)
        return first_goal_minute if first_goal_minute != 999 else 0

    @staticmethod
    def _second_half_corners(match: Match) -> int:
        """Get second half corners from match data"""
        return match.second_half.home_corners + match.second_half.away_corners

    @staticmethod
    def _first_half_goals(match: Match) -> int:
        """Get first half goals from match data"""
        return match.first_half.home_goals + match.first_half.away_goals

    @staticmethod
    def _second_half_goals(match: Match) -> int:
        """Get second half goals from match data"""
        return match.second_half.home_goals + match.second_half.away_goals

    @staticmethod
    def _total_corners(match: Match) -> int:
        """Get total corners from match data"""
        home_corners = match.home_stats.corner_kicks if match.home_stats else 0
        away_corners = match.away_stats.corner_kicks if match.away_stats else 0
        return home_corners + away_corners

    @staticmethod
    def _home_corners(match: Match) -> int:
        """Get home team corners from match data"""
        return match.home_stats.corner_kicks if match.home_stats else 0

    @staticmethod
    def _away_corners(match: Match) -> int:
        """Get away team corners from match data"""
        return match.away_stats.corner_kicks if match.away_stats else 0

    @staticmethod
    def _first_half_corners(match: Match) -> int:
        """Get first half corners from match data"""
        return match.first_half.home_corners + match.first_half.away_corners

    @staticmethod
    def _first_half_result(match: Match) -> str:
        """Get first half result from match data"""
        if match.first_half.home_goals > match.first_half.away_goals:
            return "home"
        elif match.first_half.away_goals > match.first_half.home_goals:
            return "away"
        else:
            return "draw"

    @staticmethod
    def _second_half_result(match: Match) -> str:
        """Get second half result from match data"""
        if match.second_half.home_goals > match.second_half.away_goals:
            return "home"
        elif match.second_half.away_goals > match.second_half.home_goals:
            return "away"
        else:
            return "draw"

    @staticmethod
    def _has_home_score_both_halves(match: Match) -> bool:
        """Check if home team scored in both halves"""
        return match.first_half.home_goals > 0 and match.second_half.home_goals > 0

    @staticmethod
    def _has_away_score_both_halves(match: Match) -> bool:
        """Check if away team scored in both halves"""
        return match.first_half.away_goals > 0 and match.second_half.away_goals > 0

    @staticmethod
    def _home_won_either_half(match: Match) -> bool:
        """Check if home team won either half"""
        first_half_win = match.first_half.home_goals > match.first_half.away_goals
        second_half_win = match.second_half.home_goals > match.second_half.away_goals
        return first_half_win or second_half_win

    @staticmethod
    def _away_won_either_half(match: Match) -> bool:
        """Check if away team won either half"""
        first_half_win = match.first_half.away_goals > match.first_half.home_goals
        second_half_win = match.second_half.away_goals > match.second_half.home_goals
        return first_half_win or second_half_win

    @staticmethod
    def _home_won_both_halves(match: Match) -> bool:
        """Check if home team won both halves"""
        first_half_win = match.first_half.home_goals > match.first_half.away_goals
        second_half_win = match.second_half.home_goals > match.second_half.away_goals
        return first_half_win and second_half_win

    @staticmethod
    def _away_won_both_halves(match: Match) -> bool:
        """Check if away team won both halves"""
        first_half_win = match.first_half.away_goals > match.first_half.home_goals
        second_half_win = match.second_half.away_goals > match.second_half.home_goals
        return first_half_win and second_half_win

    @staticmethod
    def _highest_scoring_half(match: Match) -> str:
        """Determine which half had more goals"""
        first_half_goals = match.first_half.home_goals + match.first_half.away_goals
        second_half_goals = match.second_half.home_goals + match.second_half.away_goals

        if first_half_goals > second_half_goals:
            return "first"
        elif second_half_goals > first_half_goals:
            return "second"
        else:
            return "equal"

    @staticmethod
    def _btts_both_halves(match: Match) -> bool:
        """Check if both teams scored in both halves"""
        return EventPatterns._first_half_btts(match) and EventPatterns._second_half_btts(match)

    @staticmethod
    def _first_half_btts(match: Match) -> bool:
        """Check if both teams scored in first half"""
        return match.first_half.home_goals > 0 and match.first_half.away_goals > 0

    @staticmethod
    def _second_half_btts(match: Match) -> bool:
        """Check if both teams scored in second half"""
        return match.second_half.home_goals > 0 and match.second_half.away_goals > 0

    @staticmethod
    def _both_halves_over_1_5(match: Match) -> bool:
        """Check if both halves had over 1.5 goals"""
        first_half_goals = match.first_half.home_goals + match.first_half.away_goals
        second_half_goals = match.second_half.home_goals + match.second_half.away_goals
        return first_half_goals > 1.5 and second_half_goals > 1.5

    @staticmethod
    def _both_halves_under_1_5(match: Match) -> bool:
        """Check if both halves had under 1.5 goals"""
        first_half_goals = match.first_half.home_goals + match.first_half.away_goals
        second_half_goals = match.second_half.home_goals + match.second_half.away_goals
        return first_half_goals < 1.5 and second_half_goals < 1.5

    @staticmethod
    def _get_halftime_fulltime(match: Match) -> str:
        """Get halftime/fulltime result"""
        first_half_result = EventPatterns._first_half_result(match)
        full_time_result = "home" if match.score_home > match.score_away else "away" if match.score_away > match.score_home else "draw"
        return f"{first_half_result}_{full_time_result}"

    @staticmethod
    def _half_gg_ng(match: Match) -> str:
        """Get GG/NG for both halves"""
        first_half_btts = EventPatterns._first_half_btts(match)
        second_half_btts = EventPatterns._second_half_btts(match)

        if not first_half_btts and not second_half_btts:
            return "no_no"
        elif first_half_btts and not second_half_btts:
            return "yes_no"
        elif first_half_btts and second_half_btts:
            return "yes_yes"
        else:
            return "no_yes"

    @staticmethod
    def _any_goal_after_minute(match: Match, minute: int) -> bool:
        """Check if any goal was scored after specified minute"""
        for event in match.events:
            if event.event_type == EventType.GOALS and event.minute and event.minute > minute:
                return True
        return False

    @staticmethod
    def get_pattern_by_name(name: str) -> EventCondition:
        patterns = {p.name: p for p in EventPatterns.get_all_patterns()}
        return patterns.get(name)
