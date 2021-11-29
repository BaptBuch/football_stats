from numpy import nan
import pandas as pd
import requests
import os
from dotenv import load_dotenv, find_dotenv
from datetime import datetime

#season_df=pd.read_csv('../raw_data/season.csv')
#standings_df = pd.read_csv('../raw_data/standings.csv')

leagues_ids = [301, 82, 564, 384, 8, 9, 72]

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'.env')
env_path = find_dotenv()
load_dotenv(env_path)
token = os.getenv('API_TOKEN')


def get_previous_season_id(match):
    season_df = pd.read_csv('../raw_data/season.csv')
    current_season_id = match.get('season_id')
    row = season_df.index[season_df['season_id'] == current_season_id][0]
    return season_df.loc[row - 1]['season_id']


def get_lastyear_points(match):
    standings_df = pd.read_csv('../raw_data/standings.csv')
    standings_df.set_index('season_id', inplace=True)
    localteam_id = match.get('localteam_id')
    visitorteam_id = match.get('visitorteam_id')
    season_id = get_previous_season_id(match)
    localteam_column_name = f"{season_id}-{localteam_id}"
    visitorteam_column_name = f"{season_id}-{visitorteam_id}"
    try:
        localteam_lastyear_points = standings_df.loc[season_id,
                                                     localteam_column_name]
    except:
        localteam_lastyear_points = 40
    try:
        visitorteam_lastyear_points = standings_df.loc[season_id,
                                                       visitorteam_column_name]
    except:
        visitorteam_lastyear_points = 40
    return localteam_lastyear_points, visitorteam_lastyear_points


def get_thisyear_position(match):
    try:
        H_thisyear_position = match.get('standings')['localteam_position']
        A_thisyear_position = match.get('standings')['visitorteam_position']
    except:
        H_thisyear_position = 10
        A_thisyear_position = 11
    if (H_thisyear_position is not None) and (A_thisyear_position is not None):
        return H_thisyear_position, A_thisyear_position
    else:
        return (10, 11)


def get_ht_result_from_ht_score(match):
    try:
        ht_score = match.get('scores').get('ht_score')
        if ht_score[0] > ht_score[2]:
            return 'H'
        elif ht_score[0] < ht_score[2]:
            return 'A'
        return 'D'
    except:
        return 'D'


def get_ft_result_from_ft_score(match):
    try:
        ft_score = match.get('scores').get('ft_score')
        if ft_score[0] > ft_score[2]:
            return 'H'
        elif ft_score[0] < ft_score[2]:
            return 'A'
        return 'D'
    except:
        return 'D'


def get_game_data(list_matchs):
    '''
    Getting passed a list of dictionnaries for a series of matches,
    return main data for each game as a list of lists
    '''
    game_data = []
    for match in list_matchs:
        H_lastyear_points, A_lastyear_points = get_lastyear_points(match)
        H_thisyear_position, A_thisyear_position = get_thisyear_position(match)
        try:
            score_ht = [
                match['scores']['ht_score'][0], match['scores']['ht_score'][2]
            ]
        except:
            score_ht = ['0', '0']
        result_ht=get_ht_result_from_ht_score(match)
        try:
            score_ft = [
                match['scores']['ft_score'][0], match['scores']['ft_score'][2]
            ]
        except:
            score_ft = ['0', '0']
        result_ft=get_ft_result_from_ft_score(match)
        if datetime.strptime(
                match.get('time').get('starting_at').get('date'),
                "%Y-%m-%d") > datetime(2020, 5, 8):
            if match['league_id'] != 8:
                list_to_append = [
                    'True', match['id'], match['localteam_id'],
                    match['visitorteam_id'], match['season_id'],
                    H_lastyear_points, A_lastyear_points, H_thisyear_position,
                    A_thisyear_position, score_ht, result_ht, score_ft,
                    result_ft
                ]
        else:
            list_to_append = [
                'False', match['id'], match['localteam_id'],
                match['visitorteam_id'], match['season_id'], H_lastyear_points,
                A_lastyear_points, H_thisyear_position, A_thisyear_position,
                score_ht, result_ht, score_ft, result_ft
            ]
        match_list = []
        match_list.append(list_to_append)
        game_data.append(match_list)
    return (game_data)


def get_lineup(match):
    '''
    Getting a match as a dict, returns the starting lineup for home and away teams
    '''
    lineup_home=[0,0,0]
    lineup_away=[0,0,0]
    for index, player in enumerate(match.get('lineup').get('data')):
        if index < 11:
            if player['player']['data']['position_id']==2:
                lineup_home[0]+=1
            elif player['player']['data']['position_id']==3:
                lineup_home[1]+=1
            elif player['player']['data']['position_id']==4:
                lineup_home[2]+=1
            elif player['player']['data']['position_id']==None:
                lineup_home[1]+=1
        else:
            if player['player']['data']['position_id']==2:
                lineup_away[0]+=1
            elif player['player']['data']['position_id']==3:
                lineup_away[1]+=1
            elif player['player']['data']['position_id']==4:
                lineup_away[2]+=1
            elif player['player']['data']['position_id']==None:
                lineup_away[1]+=1

    return lineup_home, lineup_away

def get_ht_lineups(match, lineup_home, lineup_away):
    '''
    Getting a match as a dict and its starting lineups,
    return both lineups updated at half time
    '''
    home_team=str(match.get('localteam_id'))
    lineup=match.get('lineup').get('data')
    lineup_home_ht=lineup_home
    lineup_away_ht=lineup_away
    for subs in match.get('substitutions').get('data'):
        if subs['minute']<46:
            if str(subs['team_id'])==home_team:
                if subs['player']['data']['position_id']==2:
                    lineup_home_ht[0]+=1
                elif subs['player']['data']['position_id']==3:
                    lineup_home_ht[1]+=1
                elif subs['player']['data']['position_id']==4:
                    lineup_home_ht[2]+=1
                elif subs['player']['data']['position_id']==None:
                    lineup_home_ht[1]+=1
                for player in lineup:
                    if str(subs['player_out_id'])==str(player['player_id']):
                        if player['player']['data']['position_id']==2:
                            lineup_home_ht[0]-=1
                        elif player['player']['data']['position_id']==3:
                            lineup_home_ht[1]-=1
                        elif player['player']['data']['position_id']==4:
                            lineup_home_ht[2]-=1
                        else:
                            lineup_home_ht[1]-=1
            else:
                if subs['player']['data']['position_id']==2:
                    lineup_away_ht[0]+=1
                elif subs['player']['data']['position_id']==3:
                    lineup_away_ht[1]+=1
                elif subs['player']['data']['position_id']==4:
                    lineup_away_ht[2]+=1
                elif subs['player']['data']['position_id']==None:
                    lineup_away_ht[1]+=1
                for player in lineup:
                    if str(subs['player_out_id'])==str(player['player_id']):
                        if player['player']['data']['position_id']==2:
                            lineup_away_ht[0]-=1
                        elif str(player['player']['data']['position_id'])==str(3):
                            lineup_away_ht[1]-=1
                        elif player['player']['data']['position_id']==4:
                            lineup_away_ht[2]-=1
                        else:
                            lineup_away_ht[1]-=1
        return lineup_home_ht, lineup_away_ht


def get_60_lineups(match, lineup_home_ht, lineup_away_ht):
    '''
    Getting a match as a dict and its ht_lineups,
    return both lineups updated at 60'
    '''
    home_team=str(match.get('localteam_id'))
    lineup=match.get('lineup').get('data')
    lineup_home_60=lineup_home_ht
    lineup_away_60=lineup_away_ht
    for subs in match.get('substitutions').get('data'):
        if (subs['minute']>45) and (subs['minute']<61):
            if str(subs['team_id'])==home_team:
                if subs['player']['data']['position_id']==2:
                    lineup_home_60[0]+=1
                elif subs['player']['data']['position_id']==3:
                    lineup_home_60[1]+=1
                elif subs['player']['data']['position_id']==4:
                    lineup_home_60[2]+=1
                elif subs['player']['data']['position_id']==None:
                    lineup_home_60[1]+=1
                for player in lineup:
                    if str(subs['player_out_id'])==str(player['player_id']):
                        if player['player']['data']['position_id']==2:
                            lineup_home_60[0]-=1
                        elif player['player']['data']['position_id']==3:
                            lineup_home_60[1]-=1
                        elif player['player']['data']['position_id']==4:
                            lineup_home_60[2]-=1
                        else:
                            lineup_home_60[1]-=1
            else:
                if subs['player']['data']['position_id']==2:
                    lineup_away_60[0]+=1
                elif subs['player']['data']['position_id']==3:
                    lineup_away_60[1]+=1
                elif subs['player']['data']['position_id']==4:
                    lineup_away_60[2]+=1
                elif subs['player']['data']['position_id']==None:
                    lineup_away_60[1]+=1
                for player in lineup:
                    if str(subs['player_out_id'])==str(player['player_id']):
                        if player['player']['data']['position_id']==2:
                            lineup_away_60[0]-=1
                        elif str(player['player']['data']['position_id'])==str(3):
                            lineup_away_60[1]-=1
                        elif player['player']['data']['position_id']==4:
                            lineup_away_60[2]-=1
                        else:
                            lineup_away_60[1]-=1
        return lineup_home_60, lineup_away_60


def get_75_lineups(match, lineup_home_60, lineup_away_60):
    '''
    Getting a match as a dict and its 60_lineups,
    return both lineups updated at 75'
    '''
    home_team=str(match.get('localteam_id'))
    lineup=match.get('lineup').get('data')
    lineup_home_75=lineup_home_60
    lineup_away_75=lineup_away_60
    for subs in match.get('substitutions').get('data'):
        if (subs['minute']>60) and (subs['minute']<76):
            if str(subs['team_id'])==home_team:
                if subs['player']['data']['position_id']==2:
                    lineup_home_75[0]+=1
                elif subs['player']['data']['position_id']==3:
                    lineup_home_75[1]+=1
                elif subs['player']['data']['position_id']==4:
                    lineup_home_75[2]+=1
                elif subs['player']['data']['position_id']==None:
                    lineup_home_75[1]+=1
                for player in lineup:
                    if str(subs['player_out_id'])==str(player['player_id']):
                        if player['player']['data']['position_id']==2:
                            lineup_home_75[0]-=1
                        elif player['player']['data']['position_id']==3:
                            lineup_home_75[1]-=1
                        elif player['player']['data']['position_id']==4:
                            lineup_home_75[2]-=1
                        else:
                            lineup_home_75[1]-=1
            else:
                if subs['player']['data']['position_id']==2:
                    lineup_away_75[0]+=1
                elif subs['player']['data']['position_id']==3:
                    lineup_away_75[1]+=1
                elif subs['player']['data']['position_id']==4:
                    lineup_away_75[2]+=1
                elif subs['player']['data']['position_id']==None:
                    lineup_away_75[1]+=1
                for player in lineup:
                    if str(subs['player_out_id'])==str(player['player_id']):
                        if player['player']['data']['position_id']==2:
                            lineup_away_75[0]-=1
                        elif str(player['player']['data']['position_id'])==str(3):
                            lineup_away_75[1]-=1
                        elif player['player']['data']['position_id']==4:
                            lineup_away_75[2]-=1
                        else:
                            lineup_away_75[1]-=1
        return lineup_home_75, lineup_away_75


def get_90_lineups(match, lineup_home_75, lineup_away_75):
    '''
    Getting a match as a dict and its starting lineups,
    return both lineups updated at 90'
    '''
    home_team=str(match.get('localteam_id'))
    lineup=match.get('lineup').get('data')
    lineup_home = lineup_home_75
    lineup_away = lineup_away_75
    for subs in match.get('substitutions').get('data'):
        if subs['minute']>75:
            if str(subs['team_id'])==home_team:
                if subs['player']['data']['position_id']==2:
                    lineup_home[0]+=1
                elif subs['player']['data']['position_id']==3:
                    lineup_home[1]+=1
                elif subs['player']['data']['position_id']==4:
                    lineup_home[2]+=1
                elif subs['player']['data']['position_id']==None:
                    lineup_home[1]+=1
                for player in lineup:
                    if str(subs['player_out_id'])==str(player['player_id']):
                        if player['player']['data']['position_id']==2:
                            lineup_home[0]-=1
                        elif player['player']['data']['position_id']==3:
                            lineup_home[1]-=1
                        elif player['player']['data']['position_id']==4:
                            lineup_home[2]-=1
                        else:
                            lineup_home[1]-=1
            else:
                if subs['player']['data']['position_id']==2:
                    lineup_away[0]+=1
                elif subs['player']['data']['position_id']==3:
                    lineup_away[1]+=1
                elif subs['player']['data']['position_id']==4:
                    lineup_away[2]+=1
                elif subs['player']['data']['position_id']==None:
                    lineup_away[1]+=1
                for player in lineup:
                    if str(subs['player_out_id'])==str(player['player_id']):
                        if player['player']['data']['position_id']==2:
                            lineup_away[0]-=1
                        elif str(player['player']['data']['position_id'])==str(3):
                            lineup_away[1]-=1
                        elif player['player']['data']['position_id']==4:
                            lineup_away[2]-=1
                        else:
                            lineup_away[1]-=1

    return lineup_home, lineup_away

def get_all_lineups(matchs):
    '''
    Getting a list of matchs in dict form, returns a list with all the lineups
    and the evolution at different times in the game
    '''
    all_start_lineups=[]
    all_ht_lineups=[]
    all_60_lineups=[]
    all_75_lineups=[]
    all_final_lineups=[]
    for match in matchs:
        try:
            starting_lineup_home, starting_lineup_away = get_lineup(match)
            lineup_ht_home, lineup_ht_away=get_ht_lineups(match, starting_lineup_home, starting_lineup_away)
            lineup_60_home, lineup_60_away =get_60_lineups(match, lineup_ht_home, lineup_ht_away)
            lineup_75_home, lineup_75_away = get_75_lineups(match, lineup_60_home, lineup_60_away)
            final_lineup_home, final_lineup_away = get_90_lineups(match, lineup_75_home, lineup_75_away)
            all_start_lineups.append([starting_lineup_home, starting_lineup_away])
            all_ht_lineups.append([lineup_ht_home, lineup_ht_away])
            all_60_lineups.append([lineup_60_home, lineup_60_away])
            all_75_lineups.append([lineup_75_home, lineup_75_away])
            all_final_lineups.append([final_lineup_home, final_lineup_away])
        except:
            all_start_lineups.append(['NaN', 'NaN'])
            all_ht_lineups.append(['NaN', 'NaN'])
            all_60_lineups.append(['NaN', 'NaN'])
            all_75_lineups.append(['NaN', 'NaN'])
            all_final_lineups.append(['NaN', 'NaN'])
    return all_start_lineups,all_ht_lineups,all_60_lineups, all_75_lineups, all_final_lineups

def clean_lineups(list_of_lineups):
    '''
    In order to avoid unlikely values in our lineup due to lack of correct data, this function ensures that we only have
    10 players per lineup by adding 1 to the minimum value of the lineup until its sum is equal to 10
    and try to minimize the very high values by decreasing them while increasing the min value
    '''
    for lineups in list_of_lineups:
        for lineup in lineups:
            for team in lineup:
                try:
                    while sum(team)<10:
                        team[team.index(min(team))]+=1
                except:
                    continue
                for x in range(len(team)):
                    if type(team[x])==int:
                        if team[x] == 6:
                            team[team.index(min(team))]+=1
                            team[x]-=1
                        elif team[x]>6:
                            team[team.index(min(team))]+=2
                            team[x]-=2
    return list_of_lineups




def get_lineups_columns(list_of_game_data, list_of_lineups):
    '''
    Getting passed a list of game columns and a list of lineups, combine them into one list of lists
    vectors parameters allows you to decide whether you want the data for each lineup as a 3d-vector or as single values
    WARNING : the value for vectors argument should be the same for all functions
    '''
    all_rows=[]
    for i in range(len(list_of_game_data)):
        row=list_of_game_data[i]+list_of_lineups[0][i]+list_of_lineups[1][i]+list_of_lineups[2][i]+list_of_lineups[3][i]+list_of_lineups[4][i]
        all_rows.append(row)
    return all_rows

def get_flatten_rows(list_of_rows):
    '''
    Getting passed a list of lists, iterate on each element to take out each value of each lists and put them into one unique list
    to be used as row in the final dataframe
    '''
    flatten_rows=[]
    for row in list_of_rows:
        flat_list = [item for sublist in row for item in sublist]
        flatten_rows.append(flat_list)
    return flatten_rows


def get_final_df(list_of_flatten_rows):
    '''
    Getting passed a list of rows, create a dataframe
    the vectors parameter allows you to choose the adapted columns
    WARNING : the value for vectors argument should be the same for all functions
    '''
    columns = [
        'new_rules', 'game_id', 'localteam_id', 'visitorteam_id',
        'season_id', 'H_lastyear_points', 'A_lastyear_points',
        'H_thisyear_position', 'A_thisyear_position', "score_ht", "result_ht",
        "score_ft", "result_ft", "Home_D_start", "Home_M_start",
        "Home_A_start", "Away_D_start", "Away_M_start", "Away_A_start",
        "Home_D_ht", "Home_M_ht", "Home_A_ht", "Away_D_ht", "Away_M_ht",
        "Away_A_ht", "Home_D_60", "Home_M_60", "Home_A_60", "Away_D_60",
        "Away_M_60", "Away_A_60", "Home_D_75", "Home_M_75", "Home_A_75",
        "Away_D_75", "Away_M_75", "Away_A_75", "Home_D_final",
        "Home_M_final", "Home_A_final", "Away_D_final", "Away_M_final",
        "Away_A_final"
        ]
    df_lineups = pd.DataFrame(list_of_flatten_rows, columns=columns)
    return df_lineups


def collect_data_to_df(list_of_matchs):
    '''
    When passed a list of dictionnaries (each one for a game) and either new rules are true or false,
    calls all others functions to create a dataframe with all tactics and changes for
    home and away teams during a game (1 row = 1 game)
    '''

    game_columns = get_game_data(list_of_matchs)
    print("game data done")
    list_of_lineups = get_all_lineups(list_of_matchs)
    print("all lineups done")
    list_of_lineups=clean_lineups(list_of_lineups)
    print("clean lineups done")
    columns_with_lineups=get_lineups_columns(game_columns, list_of_lineups)
    flatten_rows=get_flatten_rows(columns_with_lineups)
    final_df=get_final_df(flatten_rows)
    return final_df
