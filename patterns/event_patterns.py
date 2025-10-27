from typing import List, Callable
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
            #
            # # =============================================================
            # # --- MATCH RESULT MARKETS ---
            # # =============================================================
            #
            # # --- 1x2 ---
            # EventCondition("home_win", "Home team wins", "1x2", EventType.TEAM_STATS,
            #                lambda m: m.score_home > m.score_away),
            # EventCondition("draw", "Match ends in draw", "1x2", EventType.TEAM_STATS,
            #                lambda m: m.score_home == m.score_away),
            # EventCondition("away_win", "Away team wins", "1x2", EventType.TEAM_STATS,
            #                lambda m: m.score_away > m.score_home),
            #
            # # --- double_chance ---
            # EventCondition("home_or_draw", "Home win or draw", "double_chance", EventType.TEAM_STATS,
            #                lambda m: m.score_home >= m.score_away),
            # EventCondition("home_or_away", "Home win or away win", "double_chance", EventType.TEAM_STATS,
            #                lambda m: m.score_home != m.score_away),
            # EventCondition("draw_or_away", "Draw or away win", "double_chance", EventType.TEAM_STATS,
            #                lambda m: m.score_home <= m.score_away),
            #
            # # --- draw_no_bet ---
            # EventCondition("home_win_dnb", "Home win (draw no bet)", "draw_no_bet", EventType.TEAM_STATS,
            #                lambda m: m.score_home > m.score_away),
            # EventCondition("away_win_dnb", "Away win (draw no bet)", "draw_no_bet", EventType.TEAM_STATS,
            #                lambda m: m.score_away > m.score_home),
            #
            # # --- halftime_fulltime ---
            # EventCondition("home_home", "Home/Home (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "home_home"),
            # EventCondition("home_draw", "Home/Draw (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "home_draw"),
            # EventCondition("home_away", "Home/Away (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "home_away"),
            # EventCondition("draw_home", "Draw/Home (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "draw_home"),
            # EventCondition("draw_draw", "Draw/Draw (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "draw_draw"),
            # EventCondition("draw_away", "Draw/Away (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "draw_away"),
            # EventCondition("away_home", "Away/Home (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "away_home"),
            # EventCondition("away_draw", "Away/Draw (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "away_draw"),
            # EventCondition("away_away", "Away/Away (HT/FT)", "halftime_fulltime", EventType.TEAM_STATS,
            #                lambda m: EventPatterns._get_halftime_fulltime(m) == "away_away"),
            #
            # # --- home_no_bet ---
            # EventCondition("home_no_bet_draw", "Home no bet: Draw", "home_no_bet", EventType.TEAM_STATS,
            #                lambda m: m.score_home == m.score_away),
            # EventCondition("home_no_bet_away", "Home no bet: Away", "home_no_bet", EventType.TEAM_STATS,
            #                lambda m: m.score_away > m.score_home),
            #
            # # --- away_no_bet ---
            # EventCondition("away_no_bet_home", "Away no bet: Home", "away_no_bet", EventType.TEAM_STATS,
            #                lambda m: m.score_home > m.score_away),
            # EventCondition("away_no_bet_draw", "Away no bet: Draw", "away_no_bet", EventType.TEAM_STATS,
            #                lambda m: m.score_home == m.score_away),
            #
            # # =============================================================
            # # --- HALF-TIME MARKETS ---
            # # =============================================================
            #
            # # --- first_half_1x2 ---
            # EventCondition("first_half_home_win", "First half: Home win", "first_half_1x2", EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_result(m) == "home"),
            # EventCondition("first_half_draw", "First half: Draw", "first_half_1x2", EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_result(m) == "draw"),
            # EventCondition("first_half_away_win", "First half: Away win", "first_half_1x2", EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_result(m) == "away"),
            #
            # # --- first_half_over_under ---
            # EventCondition("first_half_over_0_5", "First half goals over 0.5", "first_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_goals(m) > 0.5),
            # EventCondition("first_half_over_1_5", "First half goals over 1.5", "first_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_goals(m) > 1.5),
            # EventCondition("first_half_over_2_5", "First half goals over 2.5", "first_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_goals(m) > 2.5),
            # EventCondition("first_half_under_0_5", "First half goals under 0.5", "first_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_goals(m) < 0.5),
            # EventCondition("first_half_under_1_5", "First half goals under 1.5", "first_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_goals(m) < 1.5),
            # EventCondition("first_half_under_2_5", "First half goals under 2.5", "first_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_goals(m) < 2.5),
            #
            # # --- first_half_btts ---
            # EventCondition("first_half_btts_yes", "Both teams score in first half", "first_half_btts",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_btts(m)),
            # EventCondition("first_half_btts_no", "Not both teams score in first half", "first_half_btts",
            #                EventType.HALF_STATS,
            #                lambda m: not EventPatterns._first_half_btts(m)),
            #
            # # --- first_half_double_chance ---
            # EventCondition("first_half_home_or_draw", "First half: Home or draw", "first_half_double_chance",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_result(m) in ["home", "draw"]),
            # EventCondition("first_half_home_or_away", "First half: Home or away", "first_half_double_chance",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_result(m) in ["home", "away"]),
            # EventCondition("first_half_draw_or_away", "First half: Draw or away", "first_half_double_chance",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._first_half_result(m) in ["draw", "away"]),
            #
            # # --- second_half_1x2 ---
            # EventCondition("second_half_home_win", "Second half: Home win", "second_half_1x2", EventType.HALF_STATS,
            #                lambda m: EventPatterns._second_half_result(m) == "home"),
            # EventCondition("second_half_draw", "Second half: Draw", "second_half_1x2", EventType.HALF_STATS,
            #                lambda m: EventPatterns._second_half_result(m) == "draw"),
            # EventCondition("second_half_away_win", "Second half: Away win", "second_half_1x2", EventType.HALF_STATS,
            #                lambda m: EventPatterns._second_half_result(m) == "away"),
            #
            # # --- second_half_over_under ---
            # EventCondition("second_half_over_0_5", "Second half goals over 0.5", "second_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._second_half_goals(m) > 0.5),
            # EventCondition("second_half_over_1_5", "Second half goals over 1.5", "second_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._second_half_goals(m) > 1.5),
            # EventCondition("second_half_over_2_5", "Second half goals over 2.5", "second_half_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._second_half_goals(m) > 2.5),
            #
            # # --- second_half_btts ---
            # EventCondition("second_half_btts_yes", "Both teams score in second half", "second_half_btts",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._second_half_btts(m)),
            # EventCondition("second_half_btts_no", "Not both teams score in second half", "second_half_btts",
            #                EventType.HALF_STATS,
            #                lambda m: not EventPatterns._second_half_btts(m)),
            #
            # # --- both_halves_over_under ---
            # EventCondition("both_halves_over_1_5", "Both halves over 1.5 goals", "both_halves_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._both_halves_over_1_5(m)),
            # EventCondition("both_halves_under_1_5", "Both halves under 1.5 goals", "both_halves_over_under",
            #                EventType.HALF_STATS,
            #                lambda m: EventPatterns._both_halves_under_1_5(m)),
            #
            # # --- 1st_2nd_half_gg_ng ---
            # EventCondition("half_gg_ng_no_no", "Half GG/NG: No/No", "1st_2nd_half_gg_ng", EventType.HALF_STATS,
            #                lambda m: EventPatterns._half_gg_ng(m) == "no_no"),
            # EventCondition("half_gg_ng_yes_no", "Half GG/NG: Yes/No", "1st_2nd_half_gg_ng", EventType.HALF_STATS,
            #                lambda m: EventPatterns._half_gg_ng(m) == "yes_no"),
            # EventCondition("half_gg_ng_yes_yes", "Half GG/NG: Yes/Yes", "1st_2nd_half_gg_ng", EventType.HALF_STATS,
            #                lambda m: EventPatterns._half_gg_ng(m) == "yes_yes"),
            # EventCondition("half_gg_ng_no_yes", "Half GG/NG: No/Yes", "1st_2nd_half_gg_ng", EventType.HALF_STATS,
            #                lambda m: EventPatterns._half_gg_ng(m) == "no_yes"),
            #
            # # =============================================================
            # # --- CARDS MARKETS ---
            # # =============================================================
            #
            # # --- total_cards_over_under ---
            # EventCondition("over_0_5_cards", "Total cards over 0.5", "total_cards_over_under", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) > 0.5),
            # EventCondition("over_1_5_cards", "Total cards over 1.5", "total_cards_over_under", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) > 1.5),
            # EventCondition("over_2_5_cards", "Total cards over 2.5", "total_cards_over_under", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) > 2.5),
            # EventCondition("over_3_5_cards", "Total cards over 3.5", "total_cards_over_under", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) > 3.5),
            # EventCondition("over_4_5_cards", "Total cards over 4.5", "total_cards_over_under", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) > 4.5),
            # EventCondition("over_5_5_cards", "Total cards over 5.5", "total_cards_over_under", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) > 5.5),
            #
            # # --- team_cards_over_under ---
            # EventCondition("home_over_0_5_cards", "Home team cards over 0.5", "team_cards_home", EventType.CARDS,
            #                lambda m: EventPatterns._home_cards(m) > 0.5),
            # EventCondition("home_over_1_5_cards", "Home team cards over 1.5", "team_cards_home", EventType.CARDS,
            #                lambda m: EventPatterns._home_cards(m) > 1.5),
            # EventCondition("home_over_2_5_cards", "Home team cards over 2.5", "team_cards_home", EventType.CARDS,
            #                lambda m: EventPatterns._home_cards(m) > 2.5),
            # EventCondition("away_over_0_5_cards", "Away team cards over 0.5", "team_cards_away", EventType.CARDS,
            #                lambda m: EventPatterns._away_cards(m) > 0.5),
            # EventCondition("away_over_1_5_cards", "Away team cards over 1.5", "team_cards_away", EventType.CARDS,
            #                lambda m: EventPatterns._away_cards(m) > 1.5),
            # EventCondition("away_over_2_5_cards", "Away team cards over 2.5", "team_cards_away", EventType.CARDS,
            #                lambda m: EventPatterns._away_cards(m) > 2.5),
            #
            # # --- first_half_cards_over_under ---
            # EventCondition("first_half_over_0_5_cards", "First half cards over 0.5", "first_half_cards",
            #                EventType.CARDS,
            #                lambda m: EventPatterns._first_half_cards(m) > 0.5),
            # EventCondition("first_half_over_1_5_cards", "First half cards over 1.5", "first_half_cards",
            #                EventType.CARDS,
            #                lambda m: EventPatterns._first_half_cards(m) > 1.5),
            # EventCondition("first_half_over_2_5_cards", "First half cards over 2.5", "first_half_cards",
            #                EventType.CARDS,
            #                lambda m: EventPatterns._first_half_cards(m) > 2.5),
            #
            # # --- second_half_cards_over_under ---
            # EventCondition("second_half_over_1_5_cards", "Second half cards over 1.5", "second_half_cards",
            #                EventType.CARDS,
            #                lambda m: EventPatterns._second_half_cards(m) > 1.5),
            # EventCondition("second_half_over_2_5_cards", "Second half cards over 2.5", "second_half_cards",
            #                EventType.CARDS,
            #                lambda m: EventPatterns._second_half_cards(m) > 2.5),
            # EventCondition("second_half_over_3_5_cards", "Second half cards over 3.5", "second_half_cards",
            #                EventType.CARDS,
            #                lambda m: EventPatterns._second_half_cards(m) > 3.5),
            #
            # # --- match_cards ---
            # EventCondition("match_cards_4_plus", "Match cards 4+", "match_cards", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) >= 4),
            # EventCondition("match_cards_5_plus", "Match cards 5+", "match_cards", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) >= 5),
            # EventCondition("match_cards_6_plus", "Match cards 6+", "match_cards", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) >= 6),
            # EventCondition("match_cards_7_plus", "Match cards 7+", "match_cards", EventType.CARDS,
            #                lambda m: EventPatterns._total_cards(m) >= 7),
            #
            # # =============================================================
            # # --- CORNERS MARKETS ---
            # # =============================================================
            #
            # # --- total_corners_over_under ---
            # EventCondition("over_8_5_corners", "Total corners over 8.5", "total_corners_over_under", EventType.CORNERS,
            #                lambda m: EventPatterns._total_corners(m) > 8.5),
            # EventCondition("over_9_5_corners", "Total corners over 9.5", "total_corners_over_under", EventType.CORNERS,
            #                lambda m: EventPatterns._total_corners(m) > 9.5),
            # EventCondition("over_10_5_corners", "Total corners over 10.5", "total_corners_over_under",
            #                EventType.CORNERS,
            #                lambda m: EventPatterns._total_corners(m) > 10.5),
            #
            # # --- team_corners_over_under ---
            # EventCondition("home_over_4_5_corners", "Home team corners over 4.5", "team_corners_home",
            #                EventType.CORNERS,
            #                lambda m: EventPatterns._home_corners(m) > 4.5),
            # EventCondition("home_over_5_5_corners", "Home team corners over 5.5", "team_corners_home",
            #                EventType.CORNERS,
            #                lambda m: EventPatterns._home_corners(m) > 5.5),
            # EventCondition("away_over_1_5_corners", "Away team corners over 1.5", "team_corners_away",
            #                EventType.CORNERS,
            #                lambda m: EventPatterns._away_corners(m) > 1.5),
            # EventCondition("away_over_2_5_corners", "Away team corners over 2.5", "team_corners_away",
            #                EventType.CORNERS,
            #                lambda m: EventPatterns._away_corners(m) > 2.5),
            #
            # # --- first_half_corners_over_under ---
            # EventCondition("first_half_over_3_5_corners", "First half corners over 3.5", "first_half_corners",
            #                EventType.CORNERS,
            #                lambda m: EventPatterns._first_half_corners(m) > 3.5),
            # EventCondition("first_half_over_4_5_corners", "First half corners over 4.5", "first_half_corners",
            #                EventType.CORNERS,
            #                lambda m: EventPatterns._first_half_corners(m) > 4.5),
            # EventCondition("first_half_over_5_5_corners", "First half corners over 5.5", "first_half_corners",
            #                EventType.CORNERS,
            #                lambda m: EventPatterns._first_half_corners(m) > 5.5),
            #
            # # --- corner_range ---
            # EventCondition("corner_range_0_8", "Corner range 0-8", "corner_range", EventType.CORNERS,
            #                lambda m: 0 <= EventPatterns._total_corners(m) <= 8),
            # EventCondition("corner_range_9_11", "Corner range 9-11", "corner_range", EventType.CORNERS,
            #                lambda m: 9 <= EventPatterns._total_corners(m) <= 11),
            # EventCondition("corner_range_12_plus", "Corner range 12+", "corner_range", EventType.CORNERS,
            #                lambda m: EventPatterns._total_corners(m) >= 12),
            #
            # # --- odd_even_corners ---
            # EventCondition("corners_odd", "Total corners odd", "odd_even_corners", EventType.CORNERS,
            #                lambda m: EventPatterns._total_corners(m) % 2 == 1),
            # EventCondition("corners_even", "Total corners even", "odd_even_corners", EventType.CORNERS,
            #                lambda m: EventPatterns._total_corners(m) % 2 == 0),

            # Add more patterns as needed...
        ]

    # Real data methods - these should use actual API data

    # In your EventPatterns class, update the helper methods:

    @staticmethod
    def _first_half_goals(match: Match) -> int:
        """Get first half goals from match data"""
        return match.first_half.home_goals + match.first_half.away_goals

    @staticmethod
    def _second_half_goals(match: Match) -> int:
        """Get second half goals from match data"""
        return match.second_half.home_goals + match.second_half.away_goals

    @staticmethod
    def _total_cards(match: Match) -> int:
        """Get total cards from match data"""
        home_cards = match.home_stats.yellow_cards + match.home_stats.red_cards if match.home_stats else 0
        away_cards = match.away_stats.yellow_cards + match.away_stats.red_cards if match.away_stats else 0
        return home_cards + away_cards

    @staticmethod
    def _home_cards(match: Match) -> int:
        """Get home team cards from match data"""
        return match.home_stats.yellow_cards + match.home_stats.red_cards if match.home_stats else 0

    @staticmethod
    def _away_cards(match: Match) -> int:
        """Get away team cards from match data"""
        return match.away_stats.yellow_cards + match.away_stats.red_cards if match.away_stats else 0

    @staticmethod
    def _first_half_cards(match: Match) -> int:
        """Get first half cards from match data"""
        return match.first_half.home_cards + match.first_half.away_cards

    @staticmethod
    def _second_half_cards(match: Match) -> int:
        """Get second half cards from match data"""
        return match.second_half.home_cards + match.second_half.away_cards

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
    def _second_half_corners(match: Match) -> int:
        """Get second half corners from match data"""
        return match.second_half.home_corners + match.second_half.away_corners

    @staticmethod
    def get_pattern_by_name(name: str) -> EventCondition:
        patterns = {p.name: p for p in EventPatterns.get_all_patterns()}
        return patterns.get(name)
