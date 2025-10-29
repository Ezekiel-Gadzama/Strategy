import logging
from typing import Dict, Tuple, Any
from patterns.event_patterns import EventPatterns


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

            "Corners3Way_Home": 2.04,
            "Corners3Way_Draw": 7.40,
            "Corners3Way_Away": 2.02,

            "CornerRange_0-8": 3.25,  # Estimated
            "CornerRange_9-11": 2.10,  # Estimated
            "CornerRange_12+": 2.75,  # Estimated

            "NextCorner_Home": 1.65,
            "NextCorner_Away": 2.15,

            "MostCorners_Home": 2.04,
            "MostCorners_Away": 2.02,

            "HalfMostCorners_First": 2.50,  # Estimated
            "HalfMostCorners_Second": 2.50,  # Estimated

            "CornersOddEven_Odd": 1.85,
            "CornersOddEven_Even": 1.85,

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

            # =============================================================
            # --- SHOTS MARKETS ---
            # =============================================================
            "TotalShots_Over 25.5": 1.85,
            "TotalShots_Under 25.5": 1.90,

            "HomeShots_Over 12.5": 1.67,
            "HomeShots_Over 14.5": 2.55,
            "AwayShots_Over 11.5": 1.62,
            "AwayShots_Over 13.5": 2.47,

            "ShotsOnTarget_Over 8.5": 1.72,
            "ShotsOnTarget_Under 8.5": 2.05,

            "HomeShotsOnTarget_Over 4.5": 2.02,
            "HomeShotsOnTarget_Under 4.5": 1.75,
            "AwayShotsOnTarget_Over 4.5": 2.02,  # Assuming same as home
            "AwayShotsOnTarget_Under 4.5": 1.75,  # Assuming same as home

            "FirstShotOnTarget_Home": 1.65,
            "FirstShotOnTarget_Away": 2.15,

            # =============================================================
            # --- PENALTY MARKETS ---
            # =============================================================
            "PenaltyAwarded_Yes": 3.35,
            "PenaltyAwarded_No": 1.29,

            "HomePenaltyAwarded_Yes": 4.10,  # Assuming based on team
            "AwayPenaltyAwarded_Yes": 3.80,  # Assuming based on team

            "TwoPenaltiesAwarded_Yes": 15.00,  # Estimated
            "PenaltyFirstHalf_Yes": 4.50,  # Estimated

            # =============================================================
            # --- METHOD OF GOAL SCORING ---
            # =============================================================
            "GoalMethod_Shot": 1.50,
            "GoalMethod_Header": 5.80,
            "GoalMethod_Penalty": 7.10,
            "GoalMethod_OwnGoal": 30.00,
            "GoalMethod_FreeKick": 15.50,
            "GoalMethod_NoScore": 8.50,

            # =============================================================
            # --- FIRST EVENT MARKETS ---
            # =============================================================
            "FirstEvent_ThrowIn": 1.55,
            "FirstEvent_FreeKick": 3.50,
            "FirstEvent_GoalKick": 6.50,
            "FirstEvent_Corner": 11.00,
            "FirstEvent_Goal": 50.00,

            # =============================================================
            # --- OWN GOAL MARKETS ---
            # =============================================================
            "OwnGoal_Yes": 8.00,  # Estimated

            # =============================================================
            # --- TIME OF FIRST GOAL ---
            # =============================================================
            "FirstGoalTime_Under28": 1.85,  # Estimated
            "FirstGoalTime_Over28": 1.85,  # Estimated

            "FirstGoalBefore29_Yes": 1.87,
            "FirstGoalBefore29_No": 1.88,

            "GoalAfter70_Yes": 1.87,
            "GoalAfter70_No": 1.87,

            "TimeFirstGoal_Over28": 2.15,
            "TimeFirstGoal_Under28": 1.91,
            "TimeFirstGoal_NoScore": 8.50,

            # Time of Next Goal ranges
            "TimeNextGoal_00_09": 4.10,
            "TimeNextGoal_10_19": 5.10,
            "TimeNextGoal_20_29": 6.10,
            "TimeNextGoal_30_39": 7.50,
            "TimeNextGoal_40_49": 9.00,
            "TimeNextGoal_50_59": 13.00,
            "TimeNextGoal_60_69": 16.00,
            "TimeNextGoal_70_79": 20.00,
            "TimeNextGoal_80_90plus": 20.00,
            "TimeNextGoal_NoScore": 8.50,

            # Team-specific time of next goal (using generic values)
            "TimeNextGoalHome_00_09": 6.50,
            "TimeNextGoalHome_10_19": 7.80,
            "TimeNextGoalHome_20_29": 8.50,
            "TimeNextGoalHome_30_39": 9.25,
            "TimeNextGoalHome_40_49": 9.75,
            "TimeNextGoalHome_50_59": 12.50,
            "TimeNextGoalHome_60_69": 13.50,
            "TimeNextGoalHome_70_79": 15.50,
            "TimeNextGoalHome_80_90plus": 13.00,
            "TimeNextGoalHome_NoScore": 3.35,

            "TimeNextGoalAway_00_09": 6.50,
            "TimeNextGoalAway_10_19": 7.80,
            "TimeNextGoalAway_20_29": 8.50,
            "TimeNextGoalAway_30_39": 9.25,
            "TimeNextGoalAway_40_49": 9.75,
            "TimeNextGoalAway_50_59": 12.50,
            "TimeNextGoalAway_60_69": 13.50,
            "TimeNextGoalAway_70_79": 15.50,
            "TimeNextGoalAway_80_90plus": 13.00,
            "TimeNextGoalAway_NoScore": 3.35,

            # =============================================================
            # --- NEWLY ADDED MARKETS FROM BETANO DATA ---
            # =============================================================

            # Winning Margin
            "WinningMargin_Home1": 4.25,
            "WinningMargin_Home2": 7.40,
            "WinningMargin_Home3Plus": 13.50,
            "WinningMargin_Away1": 4.25,
            "WinningMargin_Away2": 7.40,
            "WinningMargin_Away3Plus": 14.00,
            "WinningMargin_Draw": 3.20,

            # Win Both Halves
            "HomeWinBothHalves_Yes": 6.70,
            "HomeWinBothHalves_No": 1.06,
            "AwayWinBothHalves_Yes": 6.70,
            "AwayWinBothHalves_No": 1.06,

            # Exact Goals
            "ExactGoals_0": 8.25,
            "ExactGoals_1": 4.60,
            "ExactGoals_2": 3.50,
            "ExactGoals_3": 4.10,
            "ExactGoals_4": 5.90,
            "ExactGoals_5Plus": 11.00,

            # Home Exact Goals
            "HomeExactGoals_0": 4.25,
            "HomeExactGoals_1": 2.75,
            "HomeExactGoals_2": 3.35,
            "HomeExactGoals_3Plus": 3.95,

            # Away Exact Goals
            "AwayExactGoals_0": 3.70,
            "AwayExactGoals_1": 2.60,
            "AwayExactGoals_2": 3.50,
            "AwayExactGoals_3Plus": 4.70,

            # Clean Sheet
            "HomeCleanSheet_Yes": 3.55,
            "HomeCleanSheet_No": 1.22,
            "AwayCleanSheet_Yes": 4.00,
            "AwayCleanSheet_No": 1.20,

            # Goal Range
            "GoalRange_0-1": 2.16,
            "GoalRange_2-3": 1.99,
            "GoalRange_4-6": 2.48,
            "GoalRange_7Plus": 16.00,

            # Teams to Score
            "TeamsToScore_None": 8.25,
            "TeamsToScore_OnlyHome": 5.80,
            "TeamsToScore_OnlyAway": 4.00,
            "TeamsToScore_Both": 1.67,

            # First Half Cards
            "FirstHalfCards_Over0.5": 1.46,
            "FirstHalfCards_Over1.5": 2.46,
            "FirstHalfCards_Over2.5": 4.30,

            # Second Half Cards
            "SecondHalfCards_Over1.5": 1.91,
            "SecondHalfCards_Over2.5": 3.35,
            "SecondHalfCards_Over3.5": 6.50,

            # Both Teams Card
            "BothTeamsCard_Yes": 1.46,
            "BothTeamsCard_No": 2.47,

            # Card Both Halves
            "CardBothHalves_Yes": 2.46,
            "CardBothHalves_No": 1.43,

            # Yellow Cards
            "YellowCard_Yes": 1.04,
            "YellowCard_No": 7.10,
            "HomeYellowCard_Yes": 1.04,
            "AwayYellowCard_Yes": 1.25,

            # Second Yellow
            "SecondYellow_Yes": 4.10,
            "SecondYellow_No": 1.17,

            # Red Card Combinations
            "RedCardOrPenalty_Yes": 2.64,
            "RedCardOrPenalty_No": 1.38,
            "RedCardAndPenalty_Yes": 15.00,
            "RedCardAndPenalty_No": 1.01,

            # Red Card First Half
            "RedCardFirstHalf_Yes": 4.50,
            "RedCardFirstHalf_No": 1.13,

            # Straight Red Card
            "StraightRedCard_Yes": 6.00,
            "StraightRedCard_No": 1.08,

            # First Card Time
            "FirstCardBefore35_Yes": 1.87,
            "FirstCardBefore35_No": 1.88,

            # Match Cards
            "MatchCards_4Plus": 1.79,
            "MatchCards_5Plus": 2.64,
            "MatchCards_6Plus": 4.30,
            "MatchCards_7Plus": 7.50,

            # Red Cards Over/Under
            "RedCards_Over0.5": 4.10,
            "RedCards_Over1.5": 15.00,
            "RedCards_Under0.5": 1.17,
            "RedCards_Under1.5": 1.01,

            # Both Halves Over/Under
            "BothHalvesOverUnder_Over1.5": 6.70,
            "BothHalvesOverUnder_Under1.5": 1.06,

            # Half GG/NG
            "HalfGGNG_NoNo": 1.61,
            "HalfGGNG_YesNo": 5.60,
            "HalfGGNG_YesYes": 11.75,
            "HalfGGNG_NoYes": 3.75,

            # No Draw BTTS
            "NoDrawBTTS_Yes": 3.05,
            "NoDrawBTTS_No": 1.35,

            # Goal Bounds
            "GoalBounds_0": 8.25,
            "GoalBounds_0-1": 4.60,
            "GoalBounds_0-2": 3.50,
            "GoalBounds_1": 4.60,
            "GoalBounds_1-2": 3.50,
            "GoalBounds_1-3": 4.10,
            "GoalBounds_2": 3.50,
            "GoalBounds_2-3": 4.10,
            "GoalBounds_3": 4.10,
            "GoalBounds_3-4": 5.90,
            "GoalBounds_4": 5.90,
            "GoalBounds_4-5Plus": 11.00,
            "GoalBounds_5Plus": 11.00,

            # Excluded Goals
            "ExcludedGoals_0": 1.26,
            "ExcludedGoals_1": 1.85,
            "ExcludedGoals_2": 1.92,
            "ExcludedGoals_3": 1.85,
            "ExcludedGoals_4": 1.26,
            "ExcludedGoals_5Plus": 1.01,

            # BTTS Both Halves
            "BTTSBothHalves_Yes": 11.75,
            "BTTSBothHalves_No": 1.06,

            # Additional corner markets
            "FirstHalfCorners_Over3.5": 1.62,
            "FirstHalfCorners_Over4.5": 2.34,
            "FirstHalfCorners_Over5.5": 4.10,

            # Additional card markets
            "Bookings_Over0.5": 1.04,
            "Bookings_Over1.5": 1.46,

            # =============================================================
            # --- NEW CORNER ODDS FROM BETANO ---
            # =============================================================
            "Corners_Over/Under_9.5_Over": 1.85,
            "Corners_Over/Under_9.5_Under": 1.88,

            "1stHalf_Corners_Over/Under_4.5_Over": 1.88,
            "1stHalf_Corners_Over/Under_4.5_Under": 1.85,

            # Home Team Corners Over/Under
            "HomeCorners_Over/Under_2.5_Over": 1.07,
            "HomeCorners_Over/Under_3.5_Over": 1.20,
            "HomeCorners_Over/Under_4.5_Over": 1.45,
            "HomeCorners_Over/Under_5.5_Over": 1.93,
            "HomeCorners_Over/Under_6.5_Over": 2.75,
            "HomeCorners_Over/Under_7.5_Over": 4.10,
            "HomeCorners_Over/Under_8.5_Over": 6.20,
            "HomeCorners_Over/Under_9.5_Over": 8.75,

            # Away Team Corners Over/Under
            "AwayCorners_Over/Under_0.5_Over": 1.01,
            "AwayCorners_Over/Under_1.5_Over": 1.07,
            "AwayCorners_Over/Under_2.5_Over": 1.25,
            "AwayCorners_Over/Under_3.5_Over": 1.62,
            "AwayCorners_Over/Under_4.5_Over": 2.35,
            "AwayCorners_Over/Under_5.5_Over": 3.65,
            "AwayCorners_Over/Under_6.5_Over": 5.90,
            "AwayCorners_Over/Under_7.5_Over": 9.00,
            "AwayCorners_Over/Under_8.5_Over": 11.75,

            # =============================================================
            # --- NEW CARD ODDS FROM BETANO ---
            # =============================================================
            # Total Cards Over/Under
            "Bookings_Over/Under_0.5_Over": 1.04,
            "Bookings_Over/Under_0.5_Under": 7.10,
            "Bookings_Over/Under_1.5_Over": 1.17,
            "Bookings_Over/Under_1.5_Under": 4.10,
            "Bookings_Over/Under_2.5_Over": 1.45,
            "Bookings_Over/Under_2.5_Under": 2.42,
            "Bookings_Over/Under_3.5_Over": 1.79,
            "Bookings_Over/Under_3.5_Under": 1.88,
            "Bookings_Over/Under_4.5_Over": 2.85,
            "Bookings_Over/Under_4.5_Under": 1.33,
            "Bookings_Over/Under_5.5_Over": 4.20,
            "Bookings_Over/Under_5.5_Under": 1.16,

            # Red Cards Over/Under
            "RedCards_Over/Under_0.5_Over": 5.90,
            "RedCards_Over/Under_0.5_Under": 1.11,
            "RedCards_Over/Under_1.5_Over": 16.00,
            "RedCards_Over/Under_1.5_Under": 1.004,

            # First Half Cards Over/Under
            "FirstHalf_Cards_Over/Under_0.5_Over": 1.46,
            "FirstHalf_Cards_Over/Under_0.5_Under": 2.47,
            "FirstHalf_Cards_Over/Under_1.5_Over": 2.46,
            "FirstHalf_Cards_Over/Under_1.5_Under": 1.43,
            "FirstHalf_Cards_Over/Under_2.5_Over": 4.30,
            "FirstHalf_Cards_Over/Under_2.5_Under": 1.13,

            # Home Team Cards Over/Under
            "HomeCards_Over/Under_0.5_Over": 1.04,
            "HomeCards_Over/Under_0.5_Under": 7.10,
            "HomeCards_Over/Under_1.5_Over": 1.46,
            "HomeCards_Over/Under_1.5_Under": 2.47,
            "HomeCards_Over/Under_2.5_Over": 2.46,
            "HomeCards_Over/Under_2.5_Under": 1.43,

            # Away Team Cards Over/Under
            "AwayCards_Over/Under_0.5_Over": 1.25,
            "AwayCards_Over/Under_0.5_Under": 3.30,
            "AwayCards_Over/Under_1.5_Over": 1.91,
            "AwayCards_Over/Under_1.5_Under": 1.76,
            "AwayCards_Over/Under_2.5_Over": 3.35,
            "AwayCards_Over/Under_2.5_Under": 1.24,
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

            "total_goals_odd": "Odd/Even_Odd",
            "total_goals_even": "Odd/Even_Even",

            # =============================================================
            # --- HALF TIME / FULL TIME ---
            # =============================================================
            "home_home": "HalfTimeFullTime_Home/Home",
            "home_draw": "HalfTimeFullTime_Home/Draw",
            "home_away": "HalfTimeFullTime_Home/Away",
            "draw_home": "HalfTimeFullTime_Draw/Home",
            "draw_draw": "HalfTimeFullTime_Draw/Draw",
            "draw_away": "HalfTimeFullTime_Draw/Away",
            "away_home": "HalfTimeFullTime_Away/Home",
            "away_draw": "HalfTimeFullTime_Away/Draw",
            "away_away": "HalfTimeFullTime_Away/Away",

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
            "away_win_to_nil": "AwayWinToNil_Yes",

            # Win Either Half
            "home_win_either_half": "HomeWinEitherHalf_Yes",
            "away_win_either_half": "AwayWinEitherHalf_Yes",

            # Score Both Halves
            "home_score_both_halves": "HomeScoreBothHalves_Yes",
            "away_score_both_halves": "AwayScoreBothHalves_Yes",

            # No Bet
            "home_no_bet_draw": "HomeNoBet_Draw",
            "home_no_bet_away": "HomeNoBet_Away",
            "away_no_bet_home": "AwayNoBet_Home",
            "away_no_bet_draw": "AwayNoBet_Draw",

            # Highest Scoring Half
            "highest_scoring_first": "HighestScoringHalf_Overall_1st",
            "highest_scoring_second": "HighestScoringHalf_Overall_2nd",
            "highest_scoring_equal": "HighestScoringHalf_Overall_Tie",

            # =============================================================
            # --- MULTI GOALS ---
            # =============================================================
            "multigoals_1_2": "MultiGoal_1-2",
            "multigoals_1_3": "MultiGoal_1-3",
            "multigoals_1_4": "MultiGoal_1-4",
            "multigoals_2_3": "MultiGoal_2-3",
            "multigoals_2_4": "MultiGoal_2-4",
            "multigoals_3_4": "MultiGoal_3-4",
            "multigoals_4_5": "MultiGoal_4-5",
            "multigoals_5_6": "MultiGoal_5-6",
            "multigoals_7_plus": "MultiGoal_7+",
            "multigoals_no_goal": "MultiGoal_NoGoal",

            # =============================================================
            # --- CORNERS ---
            # =============================================================
            "corners_3way_home": "Corners_1X2_Home",
            "corners_3way_draw": "Corners_1X2_Draw",
            "corners_3way_away": "Corners_1X2_Away",

            "over_8_5_corners": "Corners_Over/Under_8.5_Over",
            "under_8_5_corners": "Corners_Over/Under_8.5_Under",
            "over_9_5_corners": "Corners_Over/Under_9.5_Over",
            "under_9_5_corners": "Corners_Over/Under_9.5_Under",
            "over_10_5_corners": "Corners_Over/Under_10.5_Over",
            "under_10_5_corners": "Corners_Over/Under_10.5_Under",

            "next_corner_home": "NextCorner_Home",
            "next_corner_away": "NextCorner_Away",

            "most_corners_home": "MostCorners_Home",
            "most_corners_away": "MostCorners_Away",

            "corners_odd": "CornersOddEven_Odd",
            "corners_even": "CornersOddEven_Even",

            "corner_range_0_8": "CornerRange_0-8",
            "corner_range_9_11": "CornerRange_9-11",
            "corner_range_12_plus": "CornerRange_12+",

            "home_over_4_5_corners": "HomeCorners_Over4.5",
            "home_over_5_5_corners": "HomeCorners_Over5.5",
            "away_over_1_5_corners": "AwayCorners_Over1.5",
            "away_over_2_5_corners": "AwayCorners_Over2.5",

            "first_half_over_3_5_corners": "FirstHalfCorners_Over3.5",
            "first_half_over_4_5_corners": "FirstHalfCorners_Over4.5",
            "first_half_over_5_5_corners": "FirstHalfCorners_Over5.5",

            # =============================================================
            # --- BOOKINGS / CARDS ---
            # =============================================================
            "over_0_5_cards": "Bookings_Over0.5",
            "over_1_5_cards": "Bookings_Over1.5",
            "over_2_5_cards": "Bookings_Over2.5",
            "over_3_5_cards": "Bookings_Over3.5",
            "over_4_5_cards": "Bookings_Over4.5",
            "over_5_5_cards": "Bookings_Over5.5",
            "over_6_5_cards": "Bookings_Over6.5",

            "red_card_yes": "RedCard_Yes",
            "red_card_no": "RedCard_No",

            "home_over_0_5_cards": "HomeCards_Over0.5",
            "home_over_1_5_cards": "HomeCards_Over1.5",
            "home_over_2_5_cards": "HomeCards_Over2.5",
            "away_over_0_5_cards": "AwayCards_Over0.5",
            "away_over_1_5_cards": "AwayCards_Over1.5",
            "away_over_2_5_cards": "AwayCards_Over2.5",

            "first_half_over_0_5_cards": "FirstHalfCards_Over0.5",
            "first_half_over_1_5_cards": "FirstHalfCards_Over1.5",
            "first_half_over_2_5_cards": "FirstHalfCards_Over2.5",

            "second_half_over_1_5_cards": "SecondHalfCards_Over1.5",
            "second_half_over_2_5_cards": "SecondHalfCards_Over2.5",
            "second_half_over_3_5_cards": "SecondHalfCards_Over3.5",

            "both_teams_card_yes": "BothTeamsCard_Yes",
            "both_teams_card_no": "BothTeamsCard_No",

            "card_both_halves_yes": "CardBothHalves_Yes",
            "card_both_halves_no": "CardBothHalves_No",

            # =============================================================
            # --- WINNING MARGIN ---
            # =============================================================
            "win_margin_home_1": "WinningMargin_Home1",
            "win_margin_home_2": "WinningMargin_Home2",
            "win_margin_home_3_plus": "WinningMargin_Home3Plus",
            "win_margin_away_1": "WinningMargin_Away1",
            "win_margin_away_2": "WinningMargin_Away2",
            "win_margin_away_3_plus": "WinningMargin_Away3Plus",
            "win_margin_draw": "WinningMargin_Draw",

            # =============================================================
            # --- WIN BOTH HALVES ---
            # =============================================================
            "home_win_both_halves": "HomeWinBothHalves_Yes",
            "away_win_both_halves": "AwayWinBothHalves_Yes",

            # =============================================================
            # --- EXACT GOALS ---
            # =============================================================
            "total_goals_0": "ExactGoals_0",
            "total_goals_1": "ExactGoals_1",
            "total_goals_2": "ExactGoals_2",
            "total_goals_3": "ExactGoals_3",
            "total_goals_4": "ExactGoals_4",
            "total_goals_5_plus": "ExactGoals_5Plus",

            "home_goals_0": "HomeExactGoals_0",
            "home_goals_1": "HomeExactGoals_1",
            "home_goals_2": "HomeExactGoals_2",
            "home_goals_3_plus": "HomeExactGoals_3Plus",

            "away_goals_0": "AwayExactGoals_0",
            "away_goals_1": "AwayExactGoals_1",
            "away_goals_2": "AwayExactGoals_2",
            "away_goals_3_plus": "AwayExactGoals_3Plus",

            # =============================================================
            # --- CLEAN SHEET ---
            # =============================================================
            "clean_sheet_home": "HomeCleanSheet_Yes",
            "clean_sheet_away": "AwayCleanSheet_Yes",

            # =============================================================
            # --- GOAL RANGE ---
            # =============================================================
            "goal_range_0_1": "GoalRange_0-1",
            "goal_range_2_3": "GoalRange_2-3",
            "goal_range_4_6": "GoalRange_4-6",
            "goal_range_7_plus": "GoalRange_7Plus",

            # =============================================================
            # --- TEAMS TO SCORE ---
            # =============================================================
            "teams_to_score_none": "TeamsToScore_None",
            "teams_to_score_only_home": "TeamsToScore_OnlyHome",
            "teams_to_score_only_away": "TeamsToScore_OnlyAway",
            "teams_to_score_both": "TeamsToScore_Both",

            # =============================================================
            # --- SHOTS MARKETS ---
            # =============================================================
            "total_shots_over_25_5": "TotalShots_Over 25.5",
            "total_shots_under_25_5": "TotalShots_Under 25.5",

            "home_shots_over_12_5": "HomeShots_Over 12.5",
            "home_shots_over_14_5": "HomeShots_Over 14.5",
            "away_shots_over_11_5": "AwayShots_Over 11.5",
            "away_shots_over_13_5": "AwayShots_Over 13.5",

            "shots_on_target_over_8_5": "ShotsOnTarget_Over 8.5",
            "shots_on_target_under_8_5": "ShotsOnTarget_Under 8.5",

            "home_shots_on_target_over_4_5": "HomeShotsOnTarget_Over 4.5",
            "home_shots_on_target_under_4_5": "HomeShotsOnTarget_Under 4.5",
            "away_shots_on_target_over_4_5": "AwayShotsOnTarget_Over 4.5",
            "away_shots_on_target_under_4_5": "AwayShotsOnTarget_Under 4.5",

            "first_shot_on_target_home": "FirstShotOnTarget_Home",
            "first_shot_on_target_away": "FirstShotOnTarget_Away",

            # =============================================================
            # --- PENALTY MARKETS ---
            # =============================================================
            "penalty_awarded_yes": "PenaltyAwarded_Yes",
            "penalty_awarded_no": "PenaltyAwarded_No",

            "home_penalty_awarded_yes": "HomePenaltyAwarded_Yes",
            "away_penalty_awarded_yes": "AwayPenaltyAwarded_Yes",

            "two_penalties_awarded_yes": "TwoPenaltiesAwarded_Yes",
            "penalty_first_half_yes": "PenaltyFirstHalf_Yes",

            # =============================================================
            # --- METHOD OF GOAL SCORING ---
            # =============================================================
            "goal_method_shot": "GoalMethod_Shot",
            "goal_method_header": "GoalMethod_Header",
            "goal_method_penalty": "GoalMethod_Penalty",
            "goal_method_own_goal": "GoalMethod_OwnGoal",
            "goal_method_free_kick": "GoalMethod_FreeKick",

            # =============================================================
            # --- FIRST EVENT MARKETS ---
            # =============================================================
            "first_event_throw_in": "FirstEvent_ThrowIn",
            "first_event_free_kick": "FirstEvent_FreeKick",
            "first_event_goal_kick": "FirstEvent_GoalKick",
            "first_event_corner": "FirstEvent_Corner",
            "first_event_goal": "FirstEvent_Goal",

            # =============================================================
            # --- OWN GOAL MARKETS ---
            # =============================================================
            "own_goal_yes": "OwnGoal_Yes",

            # =============================================================
            # --- TIME OF FIRST GOAL ---
            # =============================================================
            "first_goal_before_28": "FirstGoalTime_Under28",
            "first_goal_after_28": "FirstGoalTime_Over28",

            "first_goal_before_29": "FirstGoalBefore29_Yes",
            "first_goal_after_29": "FirstGoalBefore29_No",

            "goal_after_70_yes": "GoalAfter70_Yes",
            "goal_after_70_no": "GoalAfter70_No",

            "first_goal_over_28": "TimeFirstGoal_Over28",
            "first_goal_under_28": "TimeFirstGoal_Under28",
            "first_goal_no_score": "TimeFirstGoal_NoScore",

            # =============================================================
            # --- BOTH HALVES OVER/UNDER ---
            # =============================================================
            "both_halves_over_1_5": "BothHalvesOverUnder_Over1.5",
            "both_halves_under_1_5": "BothHalvesOverUnder_Under1.5",

            # =============================================================
            # --- HALF GG/NG ---
            # =============================================================
            "half_gg_ng_no_no": "HalfGGNG_NoNo",
            "half_gg_ng_yes_no": "HalfGGNG_YesNo",
            "half_gg_ng_yes_yes": "HalfGGNG_YesYes",
            "half_gg_ng_no_yes": "HalfGGNG_NoYes",

            # =============================================================
            # --- NO DRAW BTTS ---
            # =============================================================
            "no_draw_btts_yes": "NoDrawBTTS_Yes",
            "no_draw_btts_no": "NoDrawBTTS_No",

            # =============================================================
            # --- GOAL BOUNDS ---
            # =============================================================
            "goal_bounds_0": "GoalBounds_0",
            "goal_bounds_0_1": "GoalBounds_0-1",
            "goal_bounds_0_2": "GoalBounds_0-2",
            "goal_bounds_1": "GoalBounds_1",
            "goal_bounds_1_2": "GoalBounds_1-2",
            "goal_bounds_1_3": "GoalBounds_1-3",
            "goal_bounds_2": "GoalBounds_2",
            "goal_bounds_2_3": "GoalBounds_2-3",
            "goal_bounds_3": "GoalBounds_3",
            "goal_bounds_3_4": "GoalBounds_3-4",
            "goal_bounds_4": "GoalBounds_4",
            "goal_bounds_4_5_plus": "GoalBounds_4-5Plus",
            "goal_bounds_5_plus": "GoalBounds_5Plus",

            # =============================================================
            # --- EXCLUDED GOALS ---
            # =============================================================
            "excluded_goals_0": "ExcludedGoals_0",
            "excluded_goals_1": "ExcludedGoals_1",
            "excluded_goals_2": "ExcludedGoals_2",
            "excluded_goals_3": "ExcludedGoals_3",
            "excluded_goals_4": "ExcludedGoals_4",
            "excluded_goals_5_plus": "ExcludedGoals_5Plus",

            # =============================================================
            # --- YELLOW CARD MARKETS ---
            # =============================================================
            "yellow_card_yes": "YellowCard_Yes",
            "yellow_card_no": "YellowCard_No",

            "home_yellow_card_yes": "HomeYellowCard_Yes",
            "away_yellow_card_yes": "AwayYellowCard_Yes",

            "second_yellow_yes": "SecondYellow_Yes",
            "second_yellow_no": "SecondYellow_No",

            # =============================================================
            # --- RED CARD COMBINATIONS ---
            # =============================================================
            "red_card_or_penalty_yes": "RedCardOrPenalty_Yes",
            "red_card_or_penalty_no": "RedCardOrPenalty_No",

            "red_card_and_penalty_yes": "RedCardAndPenalty_Yes",
            "red_card_and_penalty_no": "RedCardAndPenalty_No",

            "red_card_first_half_yes": "RedCardFirstHalf_Yes",
            "red_card_first_half_no": "RedCardFirstHalf_No",

            "straight_red_card_yes": "StraightRedCard_Yes",
            "straight_red_card_no": "StraightRedCard_No",

            # =============================================================
            # --- FIRST CARD TIME ---
            # =============================================================
            "first_card_before_35_yes": "FirstCardBefore35_Yes",
            "first_card_before_35_no": "FirstCardBefore35_No",

            # =============================================================
            # --- MATCH CARDS ---
            # =============================================================
            "match_cards_4_plus": "MatchCards_4Plus",
            "match_cards_5_plus": "MatchCards_5Plus",
            "match_cards_6_plus": "MatchCards_6Plus",
            "match_cards_7_plus": "MatchCards_7Plus",

            # =============================================================
            # --- RED CARDS OVER/UNDER ---
            # =============================================================
            "over_0_5_red_cards": "RedCards_Over0.5",
            "over_1_5_red_cards": "RedCards_Over1.5",
            "under_0_5_red_cards": "RedCards_Under0.5",
            "under_1_5_red_cards": "RedCards_Under1.5",

            # =============================================================
            # --- BTTS BOTH HALVES ---
            # =============================================================
            "btts_both_halves_yes": "BTTSBothHalves_Yes",
            "btts_both_halves_no": "BTTSBothHalves_No",

            "home_over_2_5_corners": "HomeCorners_Over/Under_2.5_Over",
            "home_over_3_5_corners": "HomeCorners_Over/Under_3.5_Over",
            "home_over_6_5_corners": "HomeCorners_Over/Under_6.5_Over",
            "home_over_7_5_corners": "HomeCorners_Over/Under_7.5_Over",
            "home_over_8_5_corners": "HomeCorners_Over/Under_8.5_Over",
            "home_over_9_5_corners": "HomeCorners_Over/Under_9.5_Over",

            "away_over_0_5_corners": "AwayCorners_Over/Under_0.5_Over",
            "away_over_3_5_corners": "AwayCorners_Over/Under_3.5_Over",
            "away_over_4_5_corners": "AwayCorners_Over/Under_4.5_Over",
            "away_over_5_5_corners": "AwayCorners_Over/Under_5.5_Over",
            "away_over_6_5_corners": "AwayCorners_Over/Under_6.5_Over",
            "away_over_7_5_corners": "AwayCorners_Over/Under_7.5_Over",
            "away_over_8_5_corners": "AwayCorners_Over/Under_8.5_Over",

            "under_0_5_cards": "Bookings_Over/Under_0.5_Under",
            "under_1_5_cards": "Bookings_Over/Under_1.5_Under",
            "under_2_5_cards": "Bookings_Over/Under_2.5_Under",
            "under_3_5_cards": "Bookings_Over/Under_3.5_Under",
            "under_4_5_cards": "Bookings_Over/Under_4.5_Under",
            "under_5_5_cards": "Bookings_Over/Under_5.5_Under",

            "first_half_under_0_5_cards": "FirstHalf_Cards_Over/Under_0.5_Under",
            "first_half_under_1_5_cards": "FirstHalf_Cards_Over/Under_1.5_Under",
            "first_half_under_2_5_cards": "FirstHalf_Cards_Over/Under_2.5_Under",
            "home_under_0_5_cards": "HomeCards_Over/Under_0.5_Under",
            "home_under_1_5_cards": "HomeCards_Over/Under_1.5_Under",
            "home_under_2_5_cards": "HomeCards_Over/Under_2.5_Under",
            "away_under_0_5_cards": "AwayCards_Over/Under_0.5_Under",
            "away_under_1_5_cards": "AwayCards_Over/Under_1.5_Under",
            "away_under_2_5_cards": "AwayCards_Over/Under_2.5_Under",

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

        combined_probability = 1.0
        for odds in individual_odds:
            if odds > 0:
                combined_probability *= (1.0 / odds)

        # Convert back to odds
        combined_odds = 1.0 / combined_probability if combined_probability > 0 else 0.0

        # Calculate value
        actual_probability = occurrence_probability / 100.0  # Convert from percentage
        bookmaker_probability = combined_probability
        value_indicator = (actual_probability - bookmaker_probability) * 100

        return {
            'combined_odds': combined_odds,
            'individual_odds': individual_odds,
            'bookmaker_probability': bookmaker_probability * 100,
            'occurrence_probability': occurrence_probability,
            'value_indicator': value_indicator,
            'missing_odds_patterns': missing_odds,
            'is_valuable': value_indicator > 0
        }

    def get_all_pattern_odds(self) -> Dict[str, float]:
        """Get odds for all available patterns"""
        pattern_odds = {}
        for pattern_name in self.patterns_by_name.keys():
            odds = self.find_odds_for_pattern(pattern_name)
            pattern_odds[pattern_name] = odds
        return pattern_odds
