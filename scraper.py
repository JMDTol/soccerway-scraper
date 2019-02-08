from bs4 import BeautifulSoup
import requests
import re

game_data = dict.fromkeys(['week',
                           'date',
                           'home_team_name',
                           'away_team_name',
                           'home_goal_total',
                           'away_goal_total',
                           'home_goal_times',
                           'away_goal_times',
                           'referee',
                           'home_yellow_times',
                           'home_red_times',
                           'away_yellow_times',
                           'away_red_times',
                           'home_corners',
                           'away_corners',
                           'home_shots_on',
                           'away_shots_on',
                           'home_shots_wide',
                           'away_shots_wide',
                           'home_fouls',
                           'away_fouls',
                           'home_offsides',
                           'away_offsides',
                           'home_pens',
                           'away_pens',
                           'home_pen_mins',
                           'away_pen_mins'
                           ])


def clean_string(info):
    card = (str(info.contents[1]).strip())
    card = (card[:-1])
    card = int((card.split('+')[0]))
    return card


def game_week(match_soup):
    for x in match_soup.find_all("dt", string="Game week"):
        week_number = (x.find_next('dd')).text
        game_data['week'] = int(week_number)


def date_teams(match_soup):
    page_title = match_soup.title.text
    date = page_title.split(' - ')[1]
    teams = page_title.split(' - ')[0]
    home = teams.split('vs.')[0]
    home = home.strip()
    away = teams.split('vs.')[1]
    away = away.strip()

    game_data['date'] = date
    game_data['home_team_name'] = home
    game_data['away_team_name'] = away


def referee(match_soup):
    global referee_name
    for info in match_soup.find_all('dl', class_='details'):
        if info.contents[1].text == 'Referee:':
            referee_name = info.contents[3].text
        else:
            referee_name = None

    game_data['referee'] = referee_name


def home_goals(match_soup):
    home_goal_times = []
    for info in match_soup.findAll('td', class_='player player-a'):
        home_goal_mins = info.contents[1].find('span', class_='minute')
        if home_goal_mins is not None:
            home_goal_mins = int(home_goal_mins.text.split("'")[0])
            if home_goal_mins <= 90:
                home_goal_times.append(home_goal_mins)

    game_data['home_goal_total'] = len(home_goal_times)
    game_data['home_goal_times'] = home_goal_times


def away_goals(match_soup):
    away_goal_times = []
    for info in match_soup.findAll('td', class_='player player-b'):
        away_goal_mins = info.contents[1].find('span', class_='minute')
        if away_goal_mins is not None:
            away_goal_mins = int(away_goal_mins.text.split("'")[0])
            if away_goal_mins <= 90:
                away_goal_times.append(away_goal_mins)

    game_data['away_goal_total'] = len(away_goal_times)
    game_data['away_goal_times'] = away_goal_times


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

    game_data['home_yellow_times'] = home_yellow_times
    game_data['home_red_times'] = home_red_times


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

    game_data['away_yellow_times'] = away_yellow_times
    game_data['away_red_times'] = away_red_times


def home_pens(match_soup):
    home_pen_times = []
    for info in match_soup.find_all("td", class_="player player-a"):
        if '(PG)' in info.text:
            string = info.text.strip()
            string = string[:-1]
            pen = int(re.sub('[^0-9]', '', string))
            if pen <= 90:
                home_pen_times.append(pen)

    game_data['home_pen_mins'] = sum(home_pen_times)
    game_data['home_pens'] = len(home_pen_times)


def away_pens(match_soup):
    away_pen_times = []
    for info in match_soup.find_all("td", class_="player player-b"):
        if '(PG)' in info.text:
            string = info.text.strip()
            string = string[:-1]
            pen = int(re.sub('[^0-9]', '', string))
            if pen <= 90:
                away_pen_times.append(pen)

        game_data['away_pen_mins'] = sum(away_pen_times)
        game_data['away_pens'] = len(away_pen_times)


def scrape_iframe(match_soup):
    match_stats = []
    keys = ['home_corners', 'away_corners', 'home_shots_on', 'away_shots_on', 'home_shots_wide', 'away_shots_wide',
            'home_fouls', 'away_fouls', 'home_offsides', 'away_offsides']

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
            if len(match_stats) == 10:
                for i in range(10):
                    game_data[(keys[i])] = match_stats[i]
        else:
            for i in range(10):
                game_data[(keys[i])] = None


def scrape_match(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    game_week(soup)
    date_teams(soup)
    referee(soup)
    home_goals(soup)
    away_goals(soup)
    home_bookings(soup)
    away_bookings(soup)
    home_pens(soup)
    away_pens(soup)
    scrape_iframe(soup)

    return game_data
