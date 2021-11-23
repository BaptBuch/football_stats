import requests
import matplotlib.pyplot as plt

def define_request(
    token,
    start_year='2015-08-01',
    end_year='2021-11-22',
    league_ids={
        'Ligue 1': 301,
        'Bundesliga': 82,
        'La Liga': 564,
        'Serie A': 384,
        'Premier League': 8,
        'Championship': 9,
        'Eredivisie': 72
    }):
    """permet d'interroger l'api pour obtenir le json demandé en précisant le token utilisé
    les dates de début et de fin(format 'YYYY-MM-DD') et les compétitions souhaitées
    (sous la forme d'un dico {'name_of_league':league_id...}"""
    base_url = f"https://soccer.sportmonks.com/api/v2.0/fixtures/between/{start_year}/{end_year}"
    params = {
        'api_token': token,
        'include':
        f"league,stats,substitutions.player,goals,events,lineup.player&leagues={league_ids.values()}",
        'per_page': 150
    }
    rep = requests.get(url=base_url, params=params)
    if rep.status_code == 200:
        return rep.json()
    else:
        print('Error')


def count_subs(match_idx,reponse):
    """détermine le nombre de remplacements effectués dans un match connaissant son index dans reponse"""
    return len(reponse.get('data')[match_idx].get('substitutions').get('data'))


def plot_nb_of_subs(reponse):
    """plots the number of subs for the given json"""
    nb_of_subs = []
    nb_of_games = 0
    nb_of_pages = reponse.get('meta').get('pagination').get('total_pages')
    for i in range(nb_of_pages):
        nb_of_games += len(reponse.get('data'))
        for j in range(len(reponse.get('data'))):
            nb_of_subs.append(count_subs(j, reponse))
    print(f"The average number of subs is: {sum(nb_of_subs)/nb_of_games}")
    plt.hist(nb_of_subs)
    plt.ylabel('number of games')
    plt.xlabel('number of subs')

print('bonjour')
