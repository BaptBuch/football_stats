import requests
import os
import pandas as pd

token = os.getenv('API_TOKEN')
leagues_ids = [301, 82, 564, 384, 8, 9, 72]


def get_season_df():
    list_of_seasons = []
    for i in range(1, 4):
        req = requests.get(
            f'https://soccer.sportmonks.com/api/v2.0/seasons?api_token={token}&page={i}&per_page=150'
        )
        for season in req.json().get('data'):
            if season.get('league_id') in leagues_ids:
                list_of_seasons.append([
                    season.get('id'),
                    season.get('name'),
                    season.get('league_id')
                ])
    return pd.DataFrame(list_of_seasons,
                        columns=['season_id', 'name', 'league_id'])
