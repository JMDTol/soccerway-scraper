from bs4 import BeautifulSoup
from datetime import datetime
import requests


def scrape_match(url):
    """
    Create soup and scrape match data.
    :param url: Soccerway URL for match.
    :return: Dictionary containing match data
    """
    r = requests.get('https://us.' + url[11:])
    data = r.text
    soup = BeautifulSoup(data, 'html.parser')

    game_data = {}
    game_data['week'] = game_week(soup)
    game_data['date'] = date(soup)
    game_data['home_team_name'], game_data['away_team_name'] = team_names(soup)
    game_data['referee'] = referee(soup)

    home_goal_times = home_goals(soup)
    away_goal_times = away_goals(soup)
    game_data['home_goal_total'] = len(home_goal_times)
    game_data['away_goal_total'] = len(away_goal_times)
    game_data['home_goal_times'] = home_goal_times
    game_data['away_goal_times'] = away_goal_times

    game_data['home_yellow_times'], game_data['home_red_times'] = home_cards(soup)
    game_data['away_yellow_times'], game_data['away_red_times'] = away_cards(soup)

    game_data.update(scrape_iframe(soup))
    return game_data


def game_week(match_soup):
    week_elem = match_soup.find(text='Game week')
    if week_elem:
        return int(week_elem.find_next('dd').text)
    else:
        return None


def date(match_soup):
    page_title = match_soup.title.text
    date_string = page_title.split(' - ')[1]
    datetime_object = datetime.strptime(date_string, '%d %B %Y').date()
    return datetime_object


def team_names(match_soup):
    page_title = match_soup.title.text
    teams = page_title.split(' - ')[0]
    home = teams.split('vs.')[0].strip()
    away = teams.split('vs.')[1].strip()
    return home, away


def referee(match_soup):
    referee_elem = match_soup.find(text='Referee:')
    if referee_elem:
        return referee_elem.find_next('dd').text
    else:
        return None


def clean_string(time):
    time = str(time.text)
    if '+' in time:
        return int(time.split('+')[0])
    else:
        return int(time[:-1])


def home_goals(match_soup):
    goal_times = []
    for elem in match_soup.select('.player.player-a .minute'):
        goal_time = clean_string(elem)
        if goal_time <= 90:
            goal_times.append(goal_time)
    return goal_times


def away_goals(match_soup):
    goal_times = []
    for elem in match_soup.select('.player.player-b .minute'):
        goal_time = clean_string(elem)
        if goal_time <= 90:
            goal_times.append(goal_time)
    return goal_times


def home_cards(match_soup):
    yellow_times = []
    red_times = []
    for card in match_soup.select('div.container.left span'):
        if 'events/YC.png' in str(card):
            card_time = clean_string(card)
            if card_time <= 90:
                yellow_times.append(card_time)
        elif 'events/RC.png' in str(card) or 'events/Y2C.png' in str(card):
            card_time = clean_string(card)
            if card_time <= 90:
                red_times.append(card_time)
    return sorted(yellow_times), sorted(red_times)


def away_cards(match_soup):
    yellow_times = []
    red_times = []
    for card in match_soup.select('div.container.right span'):
        if 'events/YC.png' in str(card):
            card_time = clean_string(card)
            if card_time <= 90:
                yellow_times.append(card_time)
        elif 'events/RC.png' in str(card) or 'events/Y2C.png' in str(card):
            card_time = clean_string(card)
            if card_time <= 90:
                red_times.append(card_time)
    return sorted(yellow_times), sorted(red_times)


def scrape_iframe(match_soup):
    match_stats = []
    for elem in match_soup.find_all('iframe'):
        if elem['src'].startswith('/charts'):
            iframe_url = 'https://www.soccerway.com' + (elem['src'])
            iframe = requests.get(iframe_url).text
            iframe_soup = BeautifulSoup(iframe, 'html.parser')
            for stat in iframe_soup.select('.legend'):
                if 'title' not in stat.attrs['class']:
                    match_stats.append((int(stat.text)))

    keys = ('home_corners', 'away_corners', 'home_shots_on', 'away_shots_on', 'home_shots_wide', 'away_shots_wide',
            'home_fouls', 'away_fouls', 'home_offsides', 'away_offsides')

    if len(match_stats) == 10:
        return dict(zip(keys, match_stats))
    else:
        return dict.fromkeys(keys, None)
