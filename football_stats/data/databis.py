import football_stats.data
import pandas as pd

standings_df=pd.read_csv('data/standings_df.csv')


def get_lastyear_points(match):
    count_except = 0
    localteam_id = match.get('localteam_id')
    visitorteam_id = match.get('visitorteam_id')
    season_id = match.get('season_id')
    localteam_column_name = f"{season_id}_{localteam_id}_points"
    visitorteam_column_name = f"{season_id}_{visitorteam_id}_points"
    try:
        localteam_lastyear_points = standings_df.at[season_id,
                                                    localteam_column_name]
    except:
        count_except += 1
        localteam_lastyear_points = 45
    try:
        visitorteam_lastyear_points = standings_df.at[season_id,
                                                      visitorteam_column_name]
    except:
        count_except += 1
        visitorteam_lastyear_points = 45
    print(count_except)
    return localteam_lastyear_points, visitorteam_lastyear_points


def get_thisyear_position(match):
    try:
        return (match.get('standings')['localteam_position'],
                match.get('standings')['visitorteam_position'])
    except:
        return (10, 11)


