import logging
from typing import Dict, List, Tuple, Optional, Any

from data.models import EventType
from patterns.event_patterns import EventPatterns, EventCondition


class OddsCalculator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.patterns_by_name = {p.name: p for p in EventPatterns.get_all_patterns()}

        # Primary odds data from Betis vs Atletico Madrid (TOP PRIORITY)
        self.primary_odds = self._create_primary_odds_dict()

        # Fallback odds data from other matches
        self.fallback_odds = self._create_fallback_odds_dict()

    def _create_primary_odds_dict(self) -> Dict[str, float]:
        """Comprehensive Bet9ja odds for Real Betis v Atlético Madrid (27 Oct 2025)"""
        return {
            # =============================================================
            # --- MAIN 1X2 & TOTALS MARKETS ---
            # =============================================================
            "1X2_Home": 3.25,
            "1X2_Draw": 3.40,
            "1X2_Away": 2.23,

            "Over/Under_Over 0.5": 1.04,
            "Over/Under_Under 0.5": 10.50,
            "Over/Under_Over 1.5": 1.26,
            "Over/Under_Under 1.5": 3.65,
            "Over/Under_Over 2.5": 1.85,
            "Over/Under_Under 2.5": 1.92,
            "Over/Under_Over 3.5": 3.05,
            "Over/Under_Under 3.5": 1.35,
            "Over/Under_Over 4.5": 5.60,
            "Over/Under_Under 4.5": 1.11,
            "Over/Under_Over 5.5": 10.25,
            "Over/Under_Under 5.5": 1.01,
            "Over/Under_Over 6.5": 18.00,
            "Over/Under_Under 6.5": 1.00,

            # Both Teams to Score
            "GG/NG_Yes": 1.67,
            "GG/NG_No": 2.16,

            # Double Chance
            "Double Chance_Home or Draw": 1.65,
            "Double Chance_Home or Away": 1.31,
            "Double Chance_Draw or Away": 1.34,

            # Draw No Bet
            "Draw No Bet_Home": 2.31,
            "Draw No Bet_Away": 1.60,

            # Odd/Even
            "Odd/Even_Odd": 1.95,
            "Odd/Even_Even": 1.83,

            # =============================================================
            # --- HALF TIME/FULL TIME MARKETS ---
            # =============================================================
            "HalfTimeFullTime_Home/Home": 5.30,
            "HalfTimeFullTime_Home/Draw": 14.50,
            "HalfTimeFullTime_Home/Away": 27.00,
            "HalfTimeFullTime_Draw/Home": 7.70,
            "HalfTimeFullTime_Draw/Draw": 5.05,
            "HalfTimeFullTime_Draw/Away": 5.70,
            "HalfTimeFullTime_Away/Home": 33.00,
            "HalfTimeFullTime_Away/Draw": 14.75,
            "HalfTimeFullTime_Away/Away": 3.50,

            # =============================================================
            # --- FIRST HALF MARKETS ---
            # =============================================================
            "1stHalf_1X2_Home": 3.65,
            "1stHalf_1X2_Draw": 2.12,
            "1stHalf_1X2_Away": 2.75,

            "1stHalf_DoubleChance_Home or Draw": 1.34,
            "1stHalf_DoubleChance_Home or Away": 1.57,
            "1stHalf_DoubleChance_Draw or Away": 1.19,

            "1stHalf_Over/Under_Over 0.5": 1.33,
            "1stHalf_Over/Under_Under 0.5": 2.90,
            "1stHalf_Over/Under_Over 1.5": 2.65,
            "1stHalf_Over/Under_Under 1.5": 1.40,
            "1stHalf_Over/Under_Over 2.5": 6.70,
            "1stHalf_Over/Under_Under 2.5": 1.06,

            "1stHalf_GG/NG_Yes": 4.30,
            "1stHalf_GG/NG_No": 1.18,

            # =============================================================
            # --- SECOND HALF MARKETS ---
            # =============================================================
            "2ndHalf_1X2_Home": 3.40,
            "2ndHalf_1X2_Draw": 2.41,
            "2ndHalf_1X2_Away": 2.51,

            "2ndHalf_DoubleChance_Home or Draw": 1.41,
            "2ndHalf_DoubleChance_Home or Away": 1.44,
            "2ndHalf_DoubleChance_Draw or Away": 1.23,

            "2ndHalf_Over/Under_Over 0.5": 1.21,
            "2ndHalf_Over/Under_Under 0.5": 3.90,
            "2ndHalf_Over/Under_Over 1.5": 2.02,
            "2ndHalf_Over/Under_Under 1.5": 1.68,
            "2ndHalf_Over/Under_Over 2.5": 4.30,
            "2ndHalf_Over/Under_Under 2.5": 1.16,

            "2ndHalf_GG/NG_Yes": 3.10,
            "2ndHalf_GG/NG_No": 1.32,

            # =============================================================
            # --- MULTI GOAL MARKETS ---
            # =============================================================
            "MultiGoal_1-2": 2.16,
            "MultiGoal_1-3": 1.44,
            "MultiGoal_1-4": 1.16,
            "MultiGoal_1-5": 1.05,
            "MultiGoal_2-3": 1.99,
            "MultiGoal_2-4": 1.49,
            "MultiGoal_2-5": 1.32,
            "MultiGoal_3-4": 2.48,
            "MultiGoal_3-5": 2.02,
            "MultiGoal_3-6": 1.86,
            "MultiGoal_4-5": 3.80,
            "MultiGoal_4-6": 3.25,
            "MultiGoal_5-6": 7.00,

            # =============================================================
            # --- HOME / AWAY MARKETS ---
            # =============================================================
            "TeamGoals_Home_Over0.5": 1.32,
            "TeamGoals_Home_Under0.5": 3.10,
            "TeamGoals_Home_Over1.5": 2.66,
            "TeamGoals_Home_Under1.5": 1.42,
            "TeamGoals_Home_Over2.5": 6.90,
            "TeamGoals_Home_Under2.5": 1.07,

            "TeamGoals_Away_Over0.5": 1.19,
            "TeamGoals_Away_Under0.5": 4.10,
            "TeamGoals_Away_Over1.5": 2.07,
            "TeamGoals_Away_Under1.5": 1.68,
            "TeamGoals_Away_Over2.5": 4.60,
            "TeamGoals_Away_Under2.5": 1.16,

            "HomeNoBet_Draw": 2.36,
            "HomeNoBet_Away": 1.55,
            "AwayNoBet_Home": 1.83,
            "AwayNoBet_Draw": 1.91,

            "HomeWinToNil_Yes": 5.80,
            "HomeWinToNil_No": 1.09,
            "AwayWinToNil_Yes": 4.00,
            "AwayWinToNil_No": 1.19,

            "HomeWinEitherHalf_Yes": 2.07,
            "HomeWinEitherHalf_No": 1.65,
            "AwayWinEitherHalf_Yes": 1.62,
            "AwayWinEitherHalf_No": 2.12,

            "HomeScoreBothHalves_Yes": 4.35,
            "HomeScoreBothHalves_No": 1.18,
            "AwayScoreBothHalves_Yes": 3.25,
            "AwayScoreBothHalves_No": 1.29,

            "HighestScoringHalf_Home_1st": 3.55,
            "HighestScoringHalf_Home_Tie": 2.16,
            "HighestScoringHalf_Home_2nd": 2.63,
            "HighestScoringHalf_Away_1st": 3.30,
            "HighestScoringHalf_Away_Tie": 2.46,
            "HighestScoringHalf_Away_2nd": 2.41,

            # =============================================================
            # --- CORNER MARKETS ---
            # =============================================================
            "Corners_1X2_Home": 2.04,
            "Corners_1X2_Draw": 7.40,
            "Corners_1X2_Away": 2.02,

            "Corners_Over/Under_7.5_Over": 1.21,
            "Corners_Over/Under_7.5_Under": 3.65,
            "Corners_Over/Under_8.5_Over": 1.44,
            "Corners_Over/Under_8.5_Under": 2.51,
            "Corners_Over/Under_9.5_Over": 1.82,
            "Corners_Over/Under_9.5_Under": 1.90,
            "Corners_Over/Under_10.5_Over": 2.35,
            "Corners_Over/Under_10.5_Under": 1.50,
            "Corners_Over/Under_11.5_Over": 3.20,
            "Corners_Over/Under_11.5_Under": 1.26,

            "FirstCorner_Home": 1.79,
            "FirstCorner_Away": 1.82,

            "CornerOddEven_Odd": 1.85,
            "CornerOddEven_Even": 1.85,

            "LastCorner_Home": 1.79,
            "LastCorner_Away": 1.82,

            "HomeCorners_Over3.5": 1.22,
            "HomeCorners_Under3.5": 3.10,
            "HomeCorners_Over4.5": 1.62,
            "HomeCorners_Under4.5": 1.94,
            "HomeCorners_Over5.5": 2.34,
            "HomeCorners_Under5.5": 1.40,

            "AwayCorners_Over3.5": 1.24,
            "AwayCorners_Under3.5": 2.96,
            "AwayCorners_Over4.5": 1.67,
            "AwayCorners_Under4.5": 1.88,
            "AwayCorners_Over5.5": 2.44,
            "AwayCorners_Under5.5": 1.36,

            # =============================================================
            # --- BOOKINGS / CARDS MARKETS ---
            # =============================================================
            "Bookings_Over2.5": 1.06,
            "Bookings_Under2.5": 5.60,
            "Bookings_Over3.5": 1.31,
            "Bookings_Under3.5": 2.93,
            "Bookings_Over4.5": 1.79,
            "Bookings_Under4.5": 1.88,
            "Bookings_Over5.5": 2.64,
            "Bookings_Under5.5": 1.38,
            "Bookings_Over6.5": 4.30,
            "Bookings_Under6.5": 1.13,

            "1X2Cards_Home": 2.71,
            "1X2Cards_Draw": 4.95,
            "1X2Cards_Away": 1.89,

            "OddEvenCards_Odd": 1.87,
            "OddEvenCards_Even": 1.87,

            "RedCard_Yes": 4.10,
            "RedCard_No": 1.17,

            "HomeCards_Over0.5": 1.04,
            "HomeCards_Under0.5": 7.10,
            "HomeCards_Over1.5": 1.46,
            "HomeCards_Under1.5": 2.47,
            "HomeCards_Over2.5": 2.46,
            "HomeCards_Under2.5": 1.43,

            "AwayCards_Over1.5": 1.25,
            "AwayCards_Under1.5": 3.30,
            "AwayCards_Over2.5": 1.91,
            "AwayCards_Under2.5": 1.76,
            "AwayCards_Over3.5": 3.35,
            "AwayCards_Under3.5": 1.24,

            # =============================================================
            # --- SPECIAL / COMBINED MARKETS ---
            # =============================================================
            "HighestScoringHalf_Overall_1st": 3.00,
            "HighestScoringHalf_Overall_Tie": 3.55,
            "HighestScoringHalf_Overall_2nd": 2.06,

            "GoalNoGoal_HTFT_GG/GG": 11.75,
            "GoalNoGoal_HTFT_GG/NG": 5.60,
            "GoalNoGoal_HTFT_NG/GG": 3.75,
            "GoalNoGoal_HTFT_NG/NG": 1.61,

            # Multi-Goal team-specific
            "MultiGoalHome_1-2": 1.55,
            "MultiGoalHome_1-3": 1.35,
            "MultiGoalHome_2-3": 2.90,
            "MultiGoalAway_1-2": 1.54,
            "MultiGoalAway_1-3": 1.27,
            "MultiGoalAway_2-3": 2.37,
        }

    def map_pattern_to_odds_market(self, pattern_name: str) -> str:
        """Map pattern names to normalized odds market identifiers (aligned with _create_primary_odds_dict)"""
        market_mapping = {
            # =============================================================
            # --- MAIN MARKETS ---
            # =============================================================
            "home_win": "1X2_Home",
            "draw": "1X2_Draw",
            "away_win": "1X2_Away",

            "over_0_5_goals": "Over/Under_Over 0.5",
            "under_0_5_goals": "Over/Under_Under 0.5",
            "over_1_5_goals": "Over/Under_Over 1.5",
            "under_1_5_goals": "Over/Under_Under 1.5",
            "over_2_5_goals": "Over/Under_Over 2.5",
            "under_2_5_goals": "Over/Under_Under 2.5",
            "over_3_5_goals": "Over/Under_Over 3.5",
            "under_3_5_goals": "Over/Under_Under 3.5",
            "over_4_5_goals": "Over/Under_Over 4.5",
            "under_4_5_goals": "Over/Under_Under 4.5",
            "over_5_5_goals": "Over/Under_Over 5.5",
            "under_5_5_goals": "Over/Under_Under 5.5",
            "over_6_5_goals": "Over/Under_Over 6.5",
            "under_6_5_goals": "Over/Under_Under 6.5",

            "btts_yes": "GG/NG_Yes",
            "btts_no": "GG/NG_No",

            "home_or_draw": "Double Chance_Home or Draw",
            "home_or_away": "Double Chance_Home or Away",
            "draw_or_away": "Double Chance_Draw or Away",

            "home_win_dnb": "Draw No Bet_Home",
            "away_win_dnb": "Draw No Bet_Away",

            "odd_total_goals": "Odd/Even_Odd",
            "even_total_goals": "Odd/Even_Even",

            # =============================================================
            # --- HALF TIME / FULL TIME ---
            # =============================================================
            "htft_home_home": "HalfTimeFullTime_Home/Home",
            "htft_home_draw": "HalfTimeFullTime_Home/Draw",
            "htft_home_away": "HalfTimeFullTime_Home/Away",
            "htft_draw_home": "HalfTimeFullTime_Draw/Home",
            "htft_draw_draw": "HalfTimeFullTime_Draw/Draw",
            "htft_draw_away": "HalfTimeFullTime_Draw/Away",
            "htft_away_home": "HalfTimeFullTime_Away/Home",
            "htft_away_draw": "HalfTimeFullTime_Away/Draw",
            "htft_away_away": "HalfTimeFullTime_Away/Away",

            # =============================================================
            # --- FIRST HALF ---
            # =============================================================
            "first_half_home_win": "1stHalf_1X2_Home",
            "first_half_draw": "1stHalf_1X2_Draw",
            "first_half_away_win": "1stHalf_1X2_Away",

            "first_half_over_0_5": "1stHalf_Over/Under_Over 0.5",
            "first_half_under_0_5": "1stHalf_Over/Under_Under 0.5",
            "first_half_over_1_5": "1stHalf_Over/Under_Over 1.5",
            "first_half_under_1_5": "1stHalf_Over/Under_Under 1.5",
            "first_half_over_2_5": "1stHalf_Over/Under_Over 2.5",
            "first_half_under_2_5": "1stHalf_Over/Under_Under 2.5",

            "first_half_btts_yes": "1stHalf_GG/NG_Yes",
            "first_half_btts_no": "1stHalf_GG/NG_No",

            "first_half_home_or_draw": "1stHalf_DoubleChance_Home or Draw",
            "first_half_home_or_away": "1stHalf_DoubleChance_Home or Away",
            "first_half_draw_or_away": "1stHalf_DoubleChance_Draw or Away",

            # =============================================================
            # --- SECOND HALF ---
            # =============================================================
            "second_half_home_win": "2ndHalf_1X2_Home",
            "second_half_draw": "2ndHalf_1X2_Draw",
            "second_half_away_win": "2ndHalf_1X2_Away",

            "second_half_over_0_5": "2ndHalf_Over/Under_Over 0.5",
            "second_half_under_0_5": "2ndHalf_Over/Under_Under 0.5",
            "second_half_over_1_5": "2ndHalf_Over/Under_Over 1.5",
            "second_half_under_1_5": "2ndHalf_Over/Under_Under 1.5",
            "second_half_over_2_5": "2ndHalf_Over/Under_Over 2.5",
            "second_half_under_2_5": "2ndHalf_Over/Under_Under 2.5",

            "second_half_btts_yes": "2ndHalf_GG/NG_Yes",
            "second_half_btts_no": "2ndHalf_GG/NG_No",

            "second_half_home_or_draw": "2ndHalf_DoubleChance_Home or Draw",
            "second_half_home_or_away": "2ndHalf_DoubleChance_Home or Away",
            "second_half_draw_or_away": "2ndHalf_DoubleChance_Draw or Away",

            # =============================================================
            # --- TEAM GOALS ---
            # =============================================================
            "home_over_0_5": "TeamGoals_Home_Over0.5",
            "home_under_0_5": "TeamGoals_Home_Under0.5",
            "home_over_1_5": "TeamGoals_Home_Over1.5",
            "home_under_1_5": "TeamGoals_Home_Under1.5",
            "home_over_2_5": "TeamGoals_Home_Over2.5",
            "home_under_2_5": "TeamGoals_Home_Under2.5",

            "away_over_0_5": "TeamGoals_Away_Over0.5",
            "away_under_0_5": "TeamGoals_Away_Under0.5",
            "away_over_1_5": "TeamGoals_Away_Over1.5",
            "away_under_1_5": "TeamGoals_Away_Under1.5",
            "away_over_2_5": "TeamGoals_Away_Over2.5",
            "away_under_2_5": "TeamGoals_Away_Under2.5",

            # Win To Nil
            "home_win_to_nil": "HomeWinToNil_Yes",
            "home_not_win_to_nil": "HomeWinToNil_No",
            "away_win_to_nil": "AwayWinToNil_Yes",
            "away_not_win_to_nil": "AwayWinToNil_No",

            # Win Either Half
            "home_win_either_half": "HomeWinEitherHalf_Yes",
            "home_win_either_half_no": "HomeWinEitherHalf_No",
            "away_win_either_half": "AwayWinEitherHalf_Yes",
            "away_win_either_half_no": "AwayWinEitherHalf_No",

            # Score Both Halves
            "home_score_both_halves": "HomeScoreBothHalves_Yes",
            "home_score_both_halves_no": "HomeScoreBothHalves_No",
            "away_score_both_halves": "AwayScoreBothHalves_Yes",
            "away_score_both_halves_no": "AwayScoreBothHalves_No",

            # No Bet
            "home_no_bet_draw": "HomeNoBet_Draw",
            "home_no_bet_away": "HomeNoBet_Away",
            "away_no_bet_home": "AwayNoBet_Home",
            "away_no_bet_draw": "AwayNoBet_Draw",

            # Highest Scoring Half
            "highest_scoring_half_home_1st": "HighestScoringHalf_Home_1st",
            "highest_scoring_half_home_tie": "HighestScoringHalf_Home_Tie",
            "highest_scoring_half_home_2nd": "HighestScoringHalf_Home_2nd",
            "highest_scoring_half_away_1st": "HighestScoringHalf_Away_1st",
            "highest_scoring_half_away_tie": "HighestScoringHalf_Away_Tie",
            "highest_scoring_half_away_2nd": "HighestScoringHalf_Away_2nd",
            "highest_scoring_half_overall_1st": "HighestScoringHalf_Overall_1st",
            "highest_scoring_half_overall_tie": "HighestScoringHalf_Overall_Tie",
            "highest_scoring_half_overall_2nd": "HighestScoringHalf_Overall_2nd",

            # =============================================================
            # --- MULTI GOALS ---
            # =============================================================
            "multi_goal_1_2": "MultiGoal_1-2",
            "multi_goal_1_3": "MultiGoal_1-3",
            "multi_goal_1_4": "MultiGoal_1-4",
            "multi_goal_1_5": "MultiGoal_1-5",
            "multi_goal_2_3": "MultiGoal_2-3",
            "multi_goal_2_4": "MultiGoal_2-4",
            "multi_goal_2_5": "MultiGoal_2-5",
            "multi_goal_3_4": "MultiGoal_3-4",
            "multi_goal_3_5": "MultiGoal_3-5",
            "multi_goal_3_6": "MultiGoal_3-6",
            "multi_goal_4_5": "MultiGoal_4-5",
            "multi_goal_4_6": "MultiGoal_4-6",
            "multi_goal_5_6": "MultiGoal_5-6",

            "multi_goal_home_1_2": "MultiGoalHome_1-2",
            "multi_goal_home_1_3": "MultiGoalHome_1-3",
            "multi_goal_home_2_3": "MultiGoalHome_2-3",
            "multi_goal_away_1_2": "MultiGoalAway_1-2",
            "multi_goal_away_1_3": "MultiGoalAway_1-3",
            "multi_goal_away_2_3": "MultiGoalAway_2-3",

            # =============================================================
            # --- CORNERS ---
            # =============================================================
            "corners_1x2_home": "Corners_1X2_Home",
            "corners_1x2_draw": "Corners_1X2_Draw",
            "corners_1x2_away": "Corners_1X2_Away",

            "corners_over_7_5": "Corners_Over/Under_7.5_Over",
            "corners_under_7_5": "Corners_Over/Under_7.5_Under",
            "corners_over_8_5": "Corners_Over/Under_8.5_Over",
            "corners_under_8_5": "Corners_Over/Under_8.5_Under",
            "corners_over_9_5": "Corners_Over/Under_9.5_Over",
            "corners_under_9_5": "Corners_Over/Under_9.5_Under",
            "corners_over_10_5": "Corners_Over/Under_10.5_Over",
            "corners_under_10_5": "Corners_Over/Under_10.5_Under",
            "corners_over_11_5": "Corners_Over/Under_11.5_Over",
            "corners_under_11_5": "Corners_Over/Under_11.5_Under",

            "first_corner_home": "FirstCorner_Home",
            "first_corner_away": "FirstCorner_Away",
            "last_corner_home": "LastCorner_Home",
            "last_corner_away": "LastCorner_Away",

            "corner_odd_even_odd": "CornerOddEven_Odd",
            "corner_odd_even_even": "CornerOddEven_Even",

            "home_corners_over_3_5": "HomeCorners_Over3.5",
            "home_corners_under_3_5": "HomeCorners_Under3.5",
            "home_corners_over_4_5": "HomeCorners_Over4.5",
            "home_corners_under_4_5": "HomeCorners_Under4.5",
            "home_corners_over_5_5": "HomeCorners_Over5.5",
            "home_corners_under_5_5": "HomeCorners_Under5.5",
            "away_corners_over_3_5": "AwayCorners_Over3.5",
            "away_corners_under_3_5": "AwayCorners_Under3.5",
            "away_corners_over_4_5": "AwayCorners_Over4.5",
            "away_corners_under_4_5": "AwayCorners_Under4.5",
            "away_corners_over_5_5": "AwayCorners_Over5.5",
            "away_corners_under_5_5": "AwayCorners_Under5.5",

            # =============================================================
            # --- BOOKINGS / CARDS ---
            # =============================================================
            "over_2_5_cards": "Bookings_Over2.5",
            "under_2_5_cards": "Bookings_Under2.5",
            "over_3_5_cards": "Bookings_Over3.5",
            "under_3_5_cards": "Bookings_Under3.5",
            "over_4_5_cards": "Bookings_Over4.5",
            "under_4_5_cards": "Bookings_Under4.5",
            "over_5_5_cards": "Bookings_Over5.5",
            "under_5_5_cards": "Bookings_Under5.5",
            "over_6_5_cards": "Bookings_Over6.5",
            "under_6_5_cards": "Bookings_Under6.5",

            "cards_1x2_home": "1X2Cards_Home",
            "cards_1x2_draw": "1X2Cards_Draw",
            "cards_1x2_away": "1X2Cards_Away",

            "odd_even_cards_odd": "OddEvenCards_Odd",
            "odd_even_cards_even": "OddEvenCards_Even",

            "red_card_yes": "RedCard_Yes",
            "red_card_no": "RedCard_No",

            "home_cards_over_0_5": "HomeCards_Over0.5",
            "home_cards_under_0_5": "HomeCards_Under0.5",
            "home_cards_over_1_5": "HomeCards_Over1.5",
            "home_cards_under_1_5": "HomeCards_Under1.5",
            "home_cards_over_2_5": "HomeCards_Over2.5",
            "home_cards_under_2_5": "HomeCards_Under2.5",
            "away_cards_over_1_5": "AwayCards_Over1.5",
            "away_cards_under_1_5": "AwayCards_Under1.5",
            "away_cards_over_2_5": "AwayCards_Over2.5",
            "away_cards_under_2_5": "AwayCards_Under2.5",
            "away_cards_over_3_5": "AwayCards_Over3.5",
            "away_cards_under_3_5": "AwayCards_Under3.5",
        }

        return market_mapping.get(pattern_name, pattern_name)

    def _create_fallback_odds_dict(self) -> Dict[str, float]:
        """Create fallback odds dictionary from Anagennis Ierapetras vs Korfos Elountas match"""
        return {
            # 1X2 Markets
            "1x2_Home": 1.90, "1x2_Draw": 4.10, "1x2_Away": 2.75,

            # Over/Under Markets
            "Over/Under_Over 3.5": 1.70, "Over/Under_Under 3.5": 1.95,

            # Double Chance
            "Double Chance_Home or Draw": 1.30,
            "Double Chance_Home or Away": 1.12,
            "Double Chance_Draw or Away": 1.65,

            # Both Teams to Score
            "GG/NG_Yes": 1.52, "GG/NG_No": 2.30,

            # Draw No Bet
            "Draw No Bet_Home": 1.70, "Draw No Bet_Away": 2.00,

            # Correct Score
            "Correct Score_0:0": 29.00, "Correct Score_1:0": 16.00, "Correct Score_0:1": 19.50,

            # Half Time/Full Time
            "Half Time/Full Time_Home/Home": 3.85, "Half Time/Full Time_Draw/Draw": 5.40,
            "Half Time/Full Time_Away/Away": 4.55,

            # First Half Markets
            "1st Half - 1X2_Home": 2.45, "1st Half - 1X2_Draw": 2.45, "1st Half - 1X2_Away": 3.20,
            "1st Half - Over/Under_Over 0.5": 1.45, "1st Half - Over/Under_Under 0.5": 2.50,
            "1st Half - GG/NG_Yes": 4.55, "1st Half - GG/NG_No": 1.15,

            # Second Half Markets
            "2nd Half - 1X2_Home": 2.45, "2nd Half - 1X2_Draw": 3.00, "2nd Half - 1X2_Away": 2.80,
            "2nd Half - GG/NG_Yes": 2.25, "2nd Half - GG/NG_No": 1.55,

            # Team Goals
            "Home Team Goals_0": 4.25, "Home Team Goals_1": 2.75, "Home Team Goals_2": 3.35, "Home Team Goals_3+": 3.95,
            "Away Team Goals_0": 3.70, "Away Team Goals_1": 2.60, "Away Team Goals_2": 3.50, "Away Team Goals_3+": 4.70,

            # Clean Sheet
            "Home Team Clean Sheet_Yes": 3.55, "Home Team Clean Sheet_No": 1.22,
            "Away Team Clean Sheet_Yes": 4.00, "Away Team Clean Sheet_No": 1.20,

            # Exact Goals
            "Exact Goals_0": 16.50, "Exact Goals_1": 5.90, "Exact Goals_2": 3.85,
            "Exact Goals_3": 3.80, "Exact Goals_4": 4.80, "Exact Goals_5+": 4.20,

            # Odd/Even
            "Odd/Even_Odd": 1.85, "Odd/Even_Even": 1.85,
        }

    def get_latest_match_odds(self, league_id: int, season: int) -> Dict[str, float]:
        """
        Get odds for patterns - using hardcoded data
        """
        self.logger.info(f"Using hardcoded odds data for league {league_id}, season {season}")

        # Return combined odds from both primary and fallback sources
        combined_odds = {**self.fallback_odds, **self.primary_odds}

        self.logger.info(f"Returning {len(combined_odds)} odds entries")
        return combined_odds

    def find_odds_for_pattern(self, pattern_name: str) -> float:
        """Find odds for a specific pattern using primary and fallback data"""
        market_key = self.map_pattern_to_odds_market(pattern_name)

        # Try primary odds first
        if market_key in self.primary_odds:
            return self.primary_odds[market_key]

        # Try fallback odds if not found in primary
        if market_key in self.fallback_odds:
            self.logger.debug(f"Using fallback odds for {pattern_name}: {market_key}")
            return self.fallback_odds[market_key]

        # If no odds found, return neutral odds
        self.logger.debug(f"No odds found for pattern {pattern_name} (market: {market_key})")
        return 1.0

    def calculate_combination_odds(self, combination: Tuple[str, ...], occurrence_probability: float) -> Dict[str, Any]:
        """Calculate combined odds for a combination of events with correlation adjustment"""
        individual_odds = []
        missing_odds = []
        pattern_objects = []

        # Get pattern objects and individual odds
        for pattern_name in combination:
            pattern = self.patterns_by_name.get(pattern_name)
            if pattern:
                pattern_objects.append(pattern)
            odds = self.find_odds_for_pattern(pattern_name)
            individual_odds.append(odds)
            if odds == 1.0:
                missing_odds.append(pattern_name)

        if len(pattern_objects) != len(combination):
            # Fallback to simple multiplication if we can't get pattern objects
            combined_odds = 1.0
            for odds in individual_odds:
                combined_odds *= odds

            bookmaker_probability = 1.0 / combined_odds if combined_odds > 0 else 0.0
            value_indicator = occurrence_probability - (bookmaker_probability * 100)

            return {
                'combined_odds': combined_odds,
                'individual_odds': individual_odds,
                'bookmaker_probability': bookmaker_probability * 100,
                'occurrence_probability': occurrence_probability,
                'value_indicator': value_indicator,
                'missing_odds_patterns': missing_odds,
                'is_valuable': value_indicator > 0,
                'correlation_adjustment': 1.0,  # No adjustment in fallback
                'adjustment_reason': "fallback_calculation"
            }

        # Calculate correlation factors between patterns
        correlation_factors = self._calculate_correlation_factors(pattern_objects)

        # Start with independent probability assumption
        independent_combined_probability = 1.0
        for odds in individual_odds:
            if odds > 0:
                independent_combined_probability *= (1.0 / odds)

        # Apply correlation adjustment
        correlation_adjustment = self._get_correlation_adjustment(correlation_factors)
        adjusted_combined_probability = independent_combined_probability * correlation_adjustment

        # Convert back to odds
        combined_odds = 1.0 / adjusted_combined_probability if adjusted_combined_probability > 0 else 0.0

        # Calculate value
        actual_probability = occurrence_probability / 100.0  # Convert from percentage
        bookmaker_probability = adjusted_combined_probability
        value_indicator = (actual_probability - bookmaker_probability) * 100

        return {
            'combined_odds': combined_odds,
            'individual_odds': individual_odds,
            'bookmaker_probability': bookmaker_probability * 100,
            'occurrence_probability': occurrence_probability,
            'value_indicator': value_indicator,
            'missing_odds_patterns': missing_odds,
            'is_valuable': value_indicator > 0,
            'correlation_adjustment': correlation_adjustment,
            'adjustment_reason': self._get_adjustment_reason(correlation_factors),
            'correlation_details': correlation_factors
        }

    def _calculate_correlation_factors(self, patterns: List[EventCondition]) -> List[Dict[str, Any]]:
        """Calculate correlation factors between patterns"""
        correlation_factors = []

        for i in range(len(patterns)):
            for j in range(i + 1, len(patterns)):
                pattern1, pattern2 = patterns[i], patterns[j]
                correlation_score = self._get_pattern_correlation(pattern1, pattern2)
                correlation_factors.append({
                    'pattern1': pattern1.name,
                    'pattern2': pattern2.name,
                    'correlation_score': correlation_score,
                    'relationship': self._describe_relationship(pattern1, pattern2)
                })

        return correlation_factors

    def _get_pattern_correlation(self, pattern1: EventCondition, pattern2: EventCondition) -> float:
        """Get correlation score between two patterns (0.0 to 1.0)"""
        # Perfect correlation (same market or highly dependent)
        if (pattern1.market == pattern2.market and
                pattern1.event_type == pattern2.event_type):
            return   # Highly correlated

        # Check for logical dependencies
        if self._are_patterns_logically_dependent(pattern1, pattern2):
            return 0.8  # Logically dependent

        # Same event type but different markets
        if pattern1.event_type == pattern2.event_type:
            return 0.6  # Moderately correlated

        # Different event types but related (e.g., goals and match result)
        if self._are_patterns_related(pattern1, pattern2):
            return 0.4  # Slightly correlated

        # Completely independent (different domains)
        return 0.1  # Mostly independent

    def _are_patterns_logically_dependent(self, pattern1: EventCondition, pattern2: EventCondition) -> bool:
        """Check if patterns have logical dependencies"""
        # Example: "over_1_5_goals" and "over_0_5_goals" are dependent
        dependent_pairs = [
            # Goals over/under dependencies
            ("over_0_5_goals", "over_1_5_goals"),
            ("over_1_5_goals", "over_2_5_goals"),
            ("over_0_5_goals", "over_2_5_goals"),

            # Team goals dependencies
            ("home_over_0_5", "home_over_1_5"),
            ("home_over_1_5", "home_over_2_5"),

            # BTTS dependencies
            ("btts_yes", "home_over_0_5"),
            ("btts_yes", "away_over_0_5"),

            # Clean sheet dependencies
            ("clean_sheet_home", "away_goals_0"),
            ("clean_sheet_away", "home_goals_0"),
        ]

        pair = (pattern1.name, pattern2.name)
        reverse_pair = (pattern2.name, pattern1.name)

        return pair in dependent_pairs or reverse_pair in dependent_pairs

    def _are_patterns_related(self, pattern1: EventCondition, pattern2: EventCondition) -> bool:
        """Check if patterns are related across different event types"""
        # Goals and match results are related
        if (pattern1.event_type == EventType.GOALS and
                pattern2.event_type == EventType.TEAM_STATS):
            return True

        # Goals and half-time stats are related
        if (pattern1.event_type == EventType.GOALS and
                pattern2.event_type == EventType.HALF_STATS):
            return True

        # Cards and corners might have some relationship
        if (pattern1.event_type == EventType.CARDS and
                pattern2.event_type == EventType.CORNERS):
            return True

        return False

    def _get_correlation_adjustment(self, correlation_factors: List[Dict[str, Any]]) -> float:
        """Calculate the correlation adjustment factor"""
        if not correlation_factors:
            return 1.0  # No adjustment for single pattern or no correlations

        # Calculate average correlation score
        avg_correlation = sum(cf['correlation_score'] for cf in correlation_factors) / len(correlation_factors)

        # Higher correlation = lower adjustment (events more likely to occur together)
        # Lower correlation = higher adjustment (events less likely to occur together)

        if avg_correlation >= 0.8:  # Highly correlated
            return 0.3  # Significant reduction in combined probability
        elif avg_correlation >= 0.6:  # Moderately correlated
            return 0.6  # Moderate reduction
        elif avg_correlation >= 0.4:  # Slightly correlated
            return 0.8  # Small reduction
        elif avg_correlation >= 0.2:  # Mostly independent
            return 0.9  # Minimal reduction
        else:  # Completely independent
            return 1.0  # No reduction - use independent probability

    def _get_adjustment_reason(self, correlation_factors: List[Dict[str, Any]]) -> str:
        """Get human-readable reason for correlation adjustment"""
        if not correlation_factors:
            return "independent_events"

        avg_correlation = sum(cf['correlation_score'] for cf in correlation_factors) / len(correlation_factors)

        if avg_correlation >= 0.8:
            return "highly_correlated_events"
        elif avg_correlation >= 0.6:
            return "moderately_correlated_events"
        elif avg_correlation >= 0.4:
            return "slightly_correlated_events"
        elif avg_correlation >= 0.2:
            return "mostly_independent_events"
        else:
            return "independent_events"

    def _describe_relationship(self, pattern1: EventCondition, pattern2: EventCondition) -> str:
        """Describe the relationship between two patterns"""
        if pattern1.market == pattern2.market and pattern1.event_type == pattern2.event_type:
            return "same_market"

        if self._are_patterns_logically_dependent(pattern1, pattern2):
            return "logically_dependent"

        if pattern1.event_type == pattern2.event_type:
            return "same_event_type"

        if self._are_patterns_related(pattern1, pattern2):
            return "related_event_types"

        return "independent"
    def get_all_pattern_odds(self) -> Dict[str, float]:
        """Get odds for all available patterns"""
        pattern_odds = {}
        for pattern_name in self.patterns_by_name.keys():
            odds = self.find_odds_for_pattern(pattern_name)
            pattern_odds[pattern_name] = odds
        return pattern_odds