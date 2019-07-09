import unittest
import requests
import datetime

from bs4 import BeautifulSoup

import scraper


class TestScraper(unittest.TestCase):
    def setUp(self):
        response = requests.get(
            "https://us.soccerway.com/matches/2019/04/12/australia/a-league/brisbane-roar-fc/wellington-phoenix/2835039/?ICID=PL_MS_06"
        )
        self.soup = BeautifulSoup(response.text, "html.parser")

    def test_week(self):
        self.assertEqual(scraper.game_week(self.soup), 25)

    def test_date(self):
        self.assertEqual(scraper.date(self.soup), datetime.date(2019, 4, 12))

    def test_team_names(self):
        self.assertEqual(
            scraper.team_names(self.soup), ("Brisbane Roar", "Wellington Phoenix")
        )

    def test_referee(self):
        self.assertEqual(scraper.referee(self.soup), "P. Green")

    def test_home_goals(self):
        self.assertEqual(scraper.home_goals(self.soup), [37, 42])

    def test_away_goals(self):
        self.assertEqual(scraper.away_goals(self.soup), [53])

    def test_home_yellow_cards(self):
        self.assertEqual(scraper.home_yellow_cards(self.soup), [32, 34, 83, 90])

    def test_away_yellow_cards(self):
        self.assertEqual(scraper.away_yellow_cards(self.soup), [63])

    def test_home_red_cards(self):
        self.assertEqual(scraper.home_red_cards(self.soup), [90])

    def test_away_red_cards(self):
        self.assertEqual(scraper.away_red_cards(self.soup), [])

    def test_stats(self):
        self.assertEqual(
            scraper.scrape_iframe(self.soup),
            {
                "away_corners": 6,
                "away_fouls": 18,
                "away_offsides": 0,
                "away_shots_on": 4,
                "away_shots_wide": 8,
                "home_corners": 6,
                "home_fouls": 19,
                "home_offsides": 2,
                "home_shots_on": 6,
                "home_shots_wide": 11,
            },
        )
