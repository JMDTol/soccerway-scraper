from bs4 import BeautifulSoup
import requests


def clean_string(info):
    card = (str(info.contents[1]).strip())
    card = (card[:-1])
    card = int((card.split('+')[0]))
    return card


def soccerway_scraper(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

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

    # Empty lists to be populated by minute stats.
    home_goals = []
    away_goals = []
    home_yellow_times = []
    away_yellow_times = []
    home_red_times = []
    away_red_times = []
    home_pen_times = []
    away_pen_times = []

    # Find match week.
    for x in soup.find_all("dt", string="Game week"):
        week_number = (x.find_next('dd')).text
        game_data['week'] = int(week_number)

    # Scrape date and team names.
    page_title = soup.title.text
    date = page_title.split(' - ')[1]
    teams = page_title.split(' - ')[0]
    home = teams.split('vs.')[0]
    away = teams.split('vs.')[1]

    # Add date and team names to the game_data dictionary.
    game_data['date'] = date.strip()
    game_data['home_team_name'] = home.strip()
    game_data['away_team_name'] = away.strip()

    # Scrape referee name and add it to game_data.
    for info in soup.find_all('dl', class_='details'):
        if info.contents[1].text == 'Referee:':
            game_data['referee'] = info.contents[3].text
        else:
            game_data['referee'] = None

    # Scrape goal times
    for info in soup.findAll('td', class_='player player-a'):
        home_goal_mins = info.contents[1].find('span', class_='minute')
        if home_goal_mins is not None:
            home_goal_mins = int(home_goal_mins.text.split("'")[0])
            if home_goal_mins <= 90:
                home_goals.append(home_goal_mins)

    for info in soup.findAll('td', class_='player player-b'):
        away_goal_mins = info.contents[1].find('span', class_='minute')
        if away_goal_mins is not None:
            away_goal_mins = int(away_goal_mins.text.split("'")[0])
            if away_goal_mins <= 90:
                away_goals.append(away_goal_mins)

    # Add goal related markets to the game_data dictionary.
    game_data['home_goal_times'] = home_goals
    game_data['away_goal_times'] = away_goals
    game_data['home_goal_total'] = len(home_goals)
    game_data['away_goal_total'] = len(away_goals)

    # Scrape booking related markets
    for home_bookings in soup.find_all('div', {'class': 'container left'}):
        bookings = home_bookings.find_all('span')
        for info in bookings:
            if info.select('img[src*=YC]'):
                yellow = clean_string(info)
                if yellow <= 90:
                    home_yellow_times.append(yellow)
                    home_yellow_times.sort()

            elif info.select('img[src*=RC]') or info.select('img[src*=Y2C]'):
                second_yellow = clean_string(info)
                if second_yellow <= 90:
                    home_red_times.append(second_yellow)
                    home_red_times.sort()

    for away_bookings in soup.find_all('div', {'class': 'container right'}):
        bookings = away_bookings.find_all('span')
        for info in bookings:
            if info.select('img[src*=YC]'):
                yellow = clean_string(info)
                if yellow <= 90:
                    away_yellow_times.append(yellow)
                    away_yellow_times.sort()

            elif info.select('img[src*=RC]') or info.select('img[src*=Y2C]'):
                second_yellow = clean_string(info)
                if second_yellow <= 90:
                    away_red_times.append(second_yellow)
                    away_red_times.sort()

    # Add card related markets to the game_data dictionary.
    game_data['home_yellow_times'] = home_yellow_times
    game_data['home_red_times'] = home_red_times
    game_data['away_yellow_times'] = away_yellow_times
    game_data['away_red_times'] = away_red_times

    # Scrape the times of scored pens.
    for info in soup.find_all("td", class_="player player-a"):
        if '(PG)' in info.text:
            pen = (info.text.split('+')[0])
            pen = int(''.join(ch for ch in pen if ch.isdigit()))
            if pen <= 90:
                home_pen_times.append(pen)
                home_pen_times.sort()

    for info in soup.find_all("td", class_="player player-b"):
        if '(PG)' in info.text:
            pen = (info.text.split('+')[0])
            pen = int(''.join(ch for ch in pen if ch.isdigit()))
            if pen <= 90:
                away_pen_times.append(pen)
                away_pen_times.sort()

    # Add penalty related markets to game_data dictionary.
    game_data['home_pens'] = len(home_pen_times)
    game_data['away_pens'] = len(away_pen_times)
    game_data['home_pen_mins'] = sum(home_pen_times)
    game_data['away_pen_mins'] = sum(away_pen_times)

    # Scrape the iframe that contains match stats (corners, shots etc).
    match_stats = []
    keys = ['home_corners', 'away_corners', 'home_shots_on', 'away_shots_on', 'home_shots_wide', 'away_shots_wide',
            'home_fouls', 'away_fouls', 'home_offsides', 'away_offsides']

    for info in soup.find_all('iframe'):
        if info['src'].startswith('/charts'):
            iframe_complete_url = 'https://www.soccerway.com' + (info['src'])
            r = requests.get(iframe_complete_url)
            data = r.text
            iframe_soup = BeautifulSoup(data, 'html.parser')

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

    return game_data
