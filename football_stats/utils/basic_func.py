import requests
import matplotlib.pyplot as plt
import numpy as np

token = 'wuZj7IfGRn7HD2EacN7WX8KEuATaj12fyqZuHPWvFnKed06QphCKQecSuno8'
leagues_ids =['301','82','564','384','8','9','72']


def get_nbpages_url(
    token=token,
    first_day='2015-08-01',
    last_day='2021-11-22',
    league_ids=leagues_ids):
    """permet d'interroger l'api pour obtenir le nb de pages de notre requête et les params utilisés en précisant le token utilisé
    les dates de début et de fin(format 'YYYY-MM-DD') et les compétitions souhaitées
    (sous la forme d'un string d'une liste d'ids}"""
    league_ids=','.join(league_ids)
    base_url = f"https://soccer.sportmonks.com/api/v2.0/fixtures/between/{first_day}/{last_day}"
    params = {
        'api_token': token,
        'include':"league,stats,substitutions.player,goals,events,lineup.player",
        'leagues':league_ids,
        'per_page': 150
    }
    rep = requests.get(url=base_url, params=params)
    if rep.status_code == 200:
        nb_of_pages=rep.json().get('meta').get('pagination').get('total_pages')
        return (nb_of_pages,(base_url,params))
    else:
        print('Error')

def get_json_page(base_url,params,page_idx):
    params['page']=page_idx+1
    reponse=requests.get(url=base_url,params=params)
    if reponse.status_code==200:
        return reponse.json()
    else:
        print('error')


def plot_number_of_subs(token=token,
                        first_day='2015-08-01',
                        last_day='2021-11-22',
                        league_ids=leagues_ids):
    """computes the avg nb of subs and plots the number of subs"""
    base_url = f"https://soccer.sportmonks.com/api/v2.0/fixtures/between/{first_day}/{last_day}"
    nb_of_pages, params = get_nbpages_url(token=token,
                                          first_day=first_day,
                                          last_day=last_day,
                                          league_ids=leagues_ids)
    total_nb_of_games = 0
    list_nb_of_subs = []
    for i in range(nb_of_pages):
        page = get_json_page(base_url, params, i)
        nb_of_games = len(page.get('data'))
        total_nb_of_games += nb_of_games
        for j in range(nb_of_games):
            nb_of_subs = len(
                page.get('data')[j].get('substitutions').get('data'))
            list_nb_of_subs.append(nb_of_subs)
    print(
        f"The average number of subs is: {sum(list_nb_of_subs)/total_nb_of_games}"
    )
    plt.hist(list_nb_of_subs)
    plt.xlabel('nb of subs')
    plt.ylabel('nb of games')


def get_minutes_played_by_subs(match_idx, page):
    """computes the duration of subs playing for a given match_idx of a given page"""
    minutes_played_by_subs = 0
    list_of_subs = page.get('data')[match_idx].get('substitutions').get('data')
    for sub in list_of_subs:
        if sub.get('minute') < 95:
            minutes_played_by_subs += 95 - sub.get('minute')
    return minutes_played_by_subs


def plot_minutes_played_by_subs(token=token,
                                first_day='2015-08-01',
                                last_day='2021-11-22',
                                league_ids=leagues_ids):
    """computes the avg duration of subs playing and displays the hist plot of duration for subs playing"""
    (nb_pages, (my_url, params)) = get_nbpages_url(token,
                                                   first_day,
                                                   last_day,
                                                   league_ids=league_ids)
    list_minutes_played_by_subs = []
    total_number_of_games = 0
    for i in range(nb_pages):
        page = get_json_page(my_url, params, i)
        nb_games = len(page.get('data'))
        total_number_of_games += nb_games
        for j in range(nb_games):
            minutes_played_by_sub = get_minutes_played_by_subs(j, page)
            list_minutes_played_by_subs.append(minutes_played_by_sub)
    print(
        f"The average duration of subs playing is: {sum(list_minutes_played_by_subs)/total_number_of_games}"
    )
    plt.hist(list_minutes_played_by_subs)
    plt.xlabel("duration of subs playing")
    plt.ylabel("number of games")
