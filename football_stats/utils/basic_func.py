import requests


def define_request(
    token,
    start_year='2015-08-01',
    end_year='2021-08-01',
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
        f"league,stats,substitutions,goals,events&leagues={league_ids.values()}",
        'per_page': 150
    }
    rep = requests.get(url=base_url, params=params)
    if rep.status_code == 200:
        return rep.json().get('data')
    else:
        print('Error')


def count_subs(match_idx,reponse):
    """détermine le nombre de remplacements effectués dans un match connaissant son index dans reponse"""
    return len(reponse[match_idx].get('substitutions').get('data'))
