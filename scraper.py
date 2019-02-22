"""
Convert to class
"""

from bs4 import BeautifulSoup
import requests
import re


def scrape_match(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    game_data['week'] = game_week(soup)
    game_data['date'] = date(soup)
    game_data['home_team_name'], game_data['away_team_name'] = team_names(soup)
    game_data['referee'] = referee(soup)

    game_data['home_goal_total'], game_data['home_goal_times'] = home_goals(soup)
    game_data['away_goal_total'], game_data['away_goal_times'] = away_goals(soup)

    game_data['home_yellow_times'], game_data['home_red_times'] = home_bookings(soup)
    game_data['away_yellow_times'], game_data['away_red_times'] = away_bookings(soup)

    game_data['home_pens'], game_data['home_pen_mins'] = home_pens(soup)
    game_data['away_pens'], game_data['away_pen_mins'] = away_pens(soup)

    game_data.update(scrape_iframe(soup))

    return game_data


game_data = {}


def clean_string(info):
    card = (str(info.contents[1]).strip())
    card = (card[:-1])
    card = int((card.split('+')[0]))
    return card


def game_week(match_soup):
    week_element = match_soup.find("dt", string="Game week")
    if week_element:
        return int(week_element.find_next('dd').text)
    else:
        return None


def date(match_soup):
    page_title = match_soup.title.text
    return page_title.split(' - ')[1]


def team_names(match_soup):
    page_title = match_soup.title.text
    teams = page_title.split(' - ')[0]
    home = teams.split('vs.')[0].strip()
    away = teams.split('vs.')[1].strip()

    return home, away


def referee(match_soup):
    for info in match_soup.find_all('dl', class_='details'):
        if info.contents[1].text == 'Referee:':
            return info.contents[3].text
        else:
            return None


def home_goals(match_soup):
    home_goal_times = []
    for info in match_soup.findAll('td', class_='player player-a'):
        home_goal_mins = info.contents[1].find('span', class_='minute')
        if home_goal_mins is not None:
            home_goal_mins = int(home_goal_mins.text.split("'")[0])
            if home_goal_mins <= 90:
                home_goal_times.append(home_goal_mins)

    return len(home_goal_times), home_goal_times


def away_goals(match_soup):
    away_goal_times = []
    for info in match_soup.findAll('td', class_='player player-b'):
        away_goal_mins = info.contents[1].find('span', class_='minute')
        if away_goal_mins is not None:
            away_goal_mins = int(away_goal_mins.text.split("'")[0])
            if away_goal_mins <= 90:
                away_goal_times.append(away_goal_mins)

    return len(away_goal_times), away_goal_times


def home_bookings(match_soup):
    home_yellow_times = []
    home_red_times = []
    for bookings in match_soup.find_all('div', {'class': 'container left'}):
        card = bookings.find_all('span')
        for info in card:
            if info.select('img[src*=YC]'):
                yellow = clean_string(info)
                if yellow <= 90:
                    home_yellow_times.append(yellow)

            elif info.select('img[src*=RC]') or info.select('img[src*=Y2C]'):
                second_yellow = clean_string(info)
                if second_yellow <= 90:
                    home_red_times.append(second_yellow)

    home_yellow_times.sort()
    home_red_times.sort()

    return home_yellow_times, home_red_times


def away_bookings(match_soup):
    away_yellow_times = []
    away_red_times = []
    for bookings in match_soup.find_all('div', {'class': 'container right'}):
        card = bookings.find_all('span')
        for info in card:
            if info.select('img[src*=YC]'):
                yellow = clean_string(info)
                if yellow <= 90:
                    away_yellow_times.append(yellow)

            elif info.select('img[src*=RC]') or info.select('img[src*=Y2C]'):
                second_yellow = clean_string(info)
                if second_yellow <= 90:
                    away_red_times.append(second_yellow)

    away_yellow_times.sort()
    away_red_times.sort()

    return away_yellow_times, away_red_times


def home_pens(match_soup):
    home_pen_times = []
    for info in match_soup.find_all("td", class_="player player-a"):
        if '(PG)' in info.text:
            string = info.text.strip()
            string = string[:-1]
            pen = int(re.sub('[^0-9]', '', string))
            if pen <= 90:
                home_pen_times.append(pen)

    return len(home_pen_times), sum(home_pen_times)


def away_pens(match_soup):
    away_pen_times = []
    for info in match_soup.find_all("td", class_="player player-b"):
        if '(PG)' in info.text:
            string = info.text.strip()
            string = string[:-1]
            pen = int(re.sub('[^0-9]', '', string))
            if pen <= 90:
                away_pen_times.append(pen)

        return len(away_pen_times), sum(away_pen_times)


def scrape_iframe(match_soup):
    match_stats = []
    for info in match_soup.find_all('iframe'):
        if info['src'].startswith('/charts'):
            iframe_complete_url = 'https://www.soccerway.com' + (info['src'])
            iframe_r = requests.get(iframe_complete_url)
            iframe = iframe_r.text
            iframe_soup = BeautifulSoup(iframe, 'html.parser')

            for stat in iframe_soup.findAll('td', {'class': 'legend'}):
                try:
                    match_stats.append((int(stat.contents[0])))
                except (ValueError, IndexError):
                    continue

    keys = ('home_corners', 'away_corners', 'home_shots_on', 'away_shots_on', 'home_shots_wide', 'away_shots_wide',
            'home_fouls', 'away_fouls', 'home_offsides', 'away_offsides')

    if len(match_stats) == 10:
        return dict(zip(keys, match_stats))
    else:
        return dict.fromkeys(keys, None)
