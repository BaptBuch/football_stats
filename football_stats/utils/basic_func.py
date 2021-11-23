import requests

def define_request(token, start_year, end_year, league_ids):
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


def count_subs(match,reponse):
    """détermine le nombre de remplacements effectués dans un match connaissant son index dans le json reponse"""
    return len(reponse.json().get('data')[match].get('substitutions').get('data'))
