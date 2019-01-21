from bs4 import BeautifulSoup
import requests


def soccerway_scraper(url):
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    game_data = dict.fromkeys(['date',
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
                               'away_offsides'
                               ])

    # scrape date and team names
    page_title = soup.title.text
    date = page_title.split('-')[1]
    teams = page_title.split('-')[0]
    home = teams.split('vs.')[0]
    away = teams.split('vs.')[1]
    game_data['date'] = date.strip()
    game_data['home_team_name'] = home.strip()
    game_data['away_team_name'] = away.strip()

    # scrape ref
    for info in soup.findAll('a',
                             {'class': lambda x: x and 'referee' in x.split()}):
        game_data['referee'] = (info.contents[0])
        break

    home_goals = []
    away_goals = []

    # scrape goal times
    for info in soup.findAll('td', {'class': 'player player-a'}):
        home_goal_mins = info.contents[1].find(('span', {'class': 'minute'}))
        if home_goal_mins is not None:
            if (int(((home_goal_mins.get_text()).split("'")[0]).strip())) <= 90:
                home_goals.append(int(((home_goal_mins.get_text()).split("'")[0]).strip()))

    for info in soup.findAll('td', {'class': 'player player-b'}):
        away_goal_mins = info.contents[1].find(('span', {'class': 'minute'}))
        if away_goal_mins is not None:
            if (int(((away_goal_mins.get_text()).split("'")[0]).strip())) <= 90:
                away_goals.append(int(((away_goal_mins.get_text()).split("'")[0]).strip()))

    game_data['home_goal_times'] = home_goals
    game_data['away_goal_times'] = away_goals
    game_data['home_goal_total'] = len(home_goals)
    game_data['away_goal_total'] = len(away_goals)

    home_yellow_times = []
    away_yellow_times = []
    home_red_times = []
    away_red_times = []

    # scrape booking related markets
    for home_bookings in soup.find_all('div', {'class': 'container left'}):
        bookings = home_bookings.find_all('span')
        for info in bookings:
            if len(info.select('img[src*=YC]')) != 0:
                yellow = (str(info.contents[1]).strip())
                yellow = (yellow[:-1])
                yellow = int((yellow.split('+')[0]))
                if yellow <= 90:
                    home_yellow_times.append(yellow)
                    home_yellow_times.sort()

            elif len(info.select('img[src*=RC]')) or len(info.select('img[src*=Y2C]')) != 0:
                second_yellow = (str(info.contents[1]).strip())
                second_yellow = (second_yellow[:-1])
                second_yellow = int((second_yellow.split('+')[0]))
                if second_yellow <= 90:
                    home_red_times.append(second_yellow)
                    home_red_times.sort()

    for away_bookings in soup.find_all('div', {'class': 'container right'}):
        bookings = away_bookings.find_all("span")
        for info in bookings:
            if len(info.select('img[src*=YC]')) != 0:
                yellow = (str(info.contents[1]).strip())
                yellow = (yellow[:-1])
                yellow = int((yellow.split('+')[0]))
                if yellow <= 90:
                    away_yellow_times.append(yellow)
                    away_yellow_times.sort()

            elif len(info.select('img[src*=RC]')) or len(info.select('img[src*=Y2C]')) != 0:
                second_yellow = (str(info.contents[1]).strip())
                second_yellow = (second_yellow[:-1])
                second_yellow = int((second_yellow.split('+')[0]))
                if second_yellow <= 90:
                    away_red_times.append(second_yellow)
                    away_red_times.sort()

    game_data['home_yellow_times'] = home_yellow_times
    game_data['home_red_times'] = home_red_times
    game_data['away_yellow_times'] = away_yellow_times
    game_data['away_red_times'] = away_red_times

    # below scrapes iframe that contains match stats (corners, shots etc)
    iframe_complete_url = None

    for info in soup.find_all('iframe'):
        if info['src'].startswith('/charts'):
            iframe_complete_url = 'https://www.soccerway.com' + (info['src'])

    r = requests.get(iframe_complete_url)
    data = r.text
    iframe_soup = BeautifulSoup(data, 'html.parser')

    match_stats = []
    keys = ['home_corners', 'away_corners', 'home_shots_on', 'away_shots_on', 'home_shots_wide', 'away_shots_wide',
            'home_fouls', 'away_fouls', 'home_offsides', 'away_offsides']

    for info in iframe_soup.findAll('td',
                                    {'class': lambda x: x and 'legend' in x.split()}):
        try:
            match_stats.append((int(info.contents[0])))
        except ValueError:
            print("")

    for i in range(10):
        game_data[(keys[i])] = match_stats[i]

    return game_data
