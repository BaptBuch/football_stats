import requests
import matplotlib.pyplot as plt
import numpy as np

token = 'wuZj7IfGRn7HD2EacN7WX8KEuATaj12fyqZuHPWvFnKed06QphCKQecSuno8'
leagues_ids = {
    'Ligue 1': 301,
    'Bundesliga': 82,
    'La Liga': 564,
    'Serie A': 384,
    'Premier League': 8,
    'Championship': 9,
    'Eredivisie': 72
}


def get_nbpages_url(
    token,
    first_day='2015-08-01',
    last_day='2021-11-22',
    league_ids=leagues_ids):
    """permet d'interroger l'api pour obtenir le nb de pages de notre requête et les params utilisés en précisant le token utilisé
    les dates de début et de fin(format 'YYYY-MM-DD') et les compétitions souhaitées
    (sous la forme d'un dico {'name_of_league':league_id...}"""
    base_url = f"https://soccer.sportmonks.com/api/v2.0/fixtures/between/{first_day}/{last_day}"
    params = {
        'api_token': token,
        'include':"league,stats,substitutions.player,goals,events,lineup.player",
        'leagues':f"{league_ids.values()}",
        'per_page': 150
    }
    rep = requests.get(url=base_url, params=params)
    if rep.status_code == 200:
        nb_of_pages=rep.json().get('meta').get('pagination').get('total_pages')
        return (nb_of_pages,params)
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

