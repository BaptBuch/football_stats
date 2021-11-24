import pandas as pd
import requests
import os
from dotenv import load_dotenv, find_dotenv


env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'.env')
env_path = find_dotenv()
load_dotenv(env_path)
token = os.getenv('API_TOKEN')

def get_api_responses(token):
    response_pre_change = requests.get(f"https://soccer.sportmonks.com/api/v2.0/fixtures/between/2015-08-01/2020-05-08?api_token={token}&include=lineup.player,substitutions.player&leagues=301,82,564,384,8,9,72&per_page=150&page=1")
    response_post_change = requests.get(f"https://soccer.sportmonks.com/api/v2.0/fixtures/between/2020-08-01/2021-11-22?api_token={token}&include=lineup.player,substitutions.player&leagues=301,82,564,384,8,9,72&per_page=150")
    return response_pre_change, response_post_change

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
        if subs['minute']<45:
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

def get_60_lineups(match, lineup_home, lineup_away):
    '''
    Getting a match as a dict and its starting lineups,
    return both lineups updated at 60'
    '''
    home_team=str(match.get('localteam_id'))
    lineup=match.get('lineup').get('data')
    lineup_home_60=lineup_home
    lineup_away_60=lineup_away
    for subs in match.get('substitutions').get('data'):
        if (subs['minute']>45) and (subs['minute']<60):
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

def get_75_lineups(match, lineup_home, lineup_away):
    '''
    Getting a match as a dict and its starting lineups,
    return both lineups updated at 75'
    '''
    home_team=str(match.get('localteam_id'))
    lineup=match.get('lineup').get('data')
    lineup_home_75=lineup_home
    lineup_away_75=lineup_away
    for subs in match.get('substitutions').get('data'):
        if subs['minute']<75:
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

def get_subs(match, lineup_home, lineup_away):
    '''
    Getting a match as a dict and its starting lineups,
    return both lineups updated at 75'
    '''
    home_team=str(match.get('localteam_id'))
    lineup=match.get('lineup').get('data')
    for subs in match.get('substitutions').get('data'):
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
    except_count=0
    for match in matchs:
        try:
            starting_lineup_home, starting_lineup_away = get_lineup(match)
            lineup_ht_home, lineup_ht_away=get_ht_lineups(match, starting_lineup_home, starting_lineup_away)
            lineup_60_home, lineup_60_away =get_60_lineups(match, lineup_ht_home, lineup_ht_away)
            lineup_75_home, lineup_75_away =get_75_lineups(match, lineup_60_home, lineup_60_away)
            final_lineup_home, final_lineup_away = get_subs(match, starting_lineup_home, starting_lineup_away)
            all_start_lineups.append([starting_lineup_home, starting_lineup_away])
            all_ht_lineups.append([lineup_ht_home, lineup_ht_away])
            all_60_lineups.append([lineup_60_home, lineup_60_away])
            all_75_lineups.append([lineup_75_home, lineup_75_away])
            all_final_lineups.append([final_lineup_home, final_lineup_away])
        except:
            except_count+=1
            all_start_lineups.append(['NaN', 'NaN'])
            all_ht_lineups.append(['NaN', 'NaN'])
            all_60_lineups.append(['NaN', 'NaN'])
            all_75_lineups.append(['NaN', 'NaN'])
            all_final_lineups.append(['NaN', 'NaN'])
    return all_start_lineups,all_ht_lineups,all_60_lineups, all_75_lineups, all_final_lineups, except_count

def get_game_columns(list_matchs, new_rules='False'):
    '''
    Getting passed a list of dictionnaries for a series of matches,
    return main data for each game as a list of lists
    '''
    game_data=[]
    for x in range(len(list_matchs)):
        match = list_matchs[x]
        try:
            score_ht=[match['scores']['ht_score'][0],match['scores']['ht_score'][2]]
        except:
            score_ht=[0,0]
        try:
            if match['scores']['ht_score'][0]>match['scores']['ht_score'][2]:
                result_ht='H'
            elif match['scores']['ht_score'][0]<match['scores']['ht_score'][2]:
                result_ht='A'
            else:
                result_ht='D'
        except:
            result_ht='D'
        try:
            score_ft=[match['scores']['ft_score'][0],match['scores']['ft_score'][2]]
        except:
            score_ft=[0,0]
        try:
            if match['scores']['ft_score'][0]>match['scores']['ft_score'][2]:
                result_ft='H'
            elif match['scores']['ft_score'][0]<match['scores']['ft_score'][2]:
                result_ft='A'
            else:
                result_ft='D'
        except:
            result_ht='D'
        if new_rules=='True':
            if match['league_id']==8:
                list_to_append=['False', match['id'], match['localteam_id'],match['visitorteam_id'],score_ht, result_ht, score_ft, result_ft]
            else:
                list_to_append=['True', match['id'], match['localteam_id'],match['visitorteam_id'],score_ht, result_ht, score_ft, result_ft]
        else:
            list_to_append=['False', match['id'], match['localteam_id'],match['visitorteam_id'],score_ht, result_ht, score_ft, result_ft]
        match_list=[]
        match_list.append(list_to_append)
        game_data.append(match_list)
    return game_data

def get_lineups_columns(list_of_game_data, list_of_lineups, vectors=True):
    '''
    Getting passed a list of game columns and a list of lineups, combine them into one list of lists
    vectors parameters allows you to decide whether you want the data for each lineup as a 3d-vector or as single values
    WARNING : the value for vectors argument should be the same for all functions
    '''
    all_rows=[]
    if vectors == True:
        for i in range(len(list_of_game_data)):
            row=list_of_game_data[i]+[list_of_lineups[0][i]]+[list_of_lineups[1][i]]+[list_of_lineups[2][i]]+[list_of_lineups[3][i]]+[list_of_lineups[4][i]]
            all_rows.append(row)
    else:
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


def get_final_df(list_of_flatten_rows, vectors=True):
    '''
    Getting passed a list of rows, create a dataframe
    the vectors parameter allows you to choose the adapted columns
    WARNING : the value for vectors argument should be the same for all functions
    '''
    if vectors == True:
        columns = ['new_rules', 'game_id', 'localteam_id', 'visitorteam_id',"score_ht","result_ht","score_ft","result_ft", 'H_lineup_start', "A_lineup_start", 'H_lineup_ht', "A_lineup_ht", 'H_lineup_60', "A_lineup_60", 'H_lineup_75', "A_lineup_75", 'H_lineup_final', "A_lineup_final"]
    else:
        columns=['new_rules', 'game_id', 'localteam_id', 'visitorteam_id',"score_ht","result_ht","score_ft","result_ft","Home_D_start","Home_M_start","Home_A_start","Away_D_start","Away_M_start","Away_A_start","Home_D_ht","Home_M_ht","Home_A_ht","Away_D_ht","Away_M_ht","Away_A_ht","Home_D_60","Home_M_60","Home_A_60","Away_D_60","Away_M_60","Away_A_60","Home_D_75","Home_M_75","Home_A_75","Away_D_75","Away_M_75","Away_A_75","Home_D_final","Home_M_final","Home_A_final","Away_D_final","Away_M_final","Away_A_final"]
    df_lineups = pd.DataFrame(list_of_flatten_rows, columns=columns)
    return df_lineups


def collect_data_to_df(list_of_matchs, new_rules='False', vectors=True):
    '''
    When passed a list of dictionnaries (each one for a game) and either new rules are true or false,
    calls all others functions to create a dataframe with all tactics and changes for
    home and away teams during a game (1 row = 1 game)
    If data from after 05/08/2020 are passed, new rules should be set to 'True'
    the vectors parameter allows you to choose whether you want the data for each lineup as a 3d-vector or as single values
    WARNING : the value for vectors argument should be the same for all functions
    '''
    game_columns = get_game_columns(list_of_matchs, new_rules)
    list_of_lineups = get_all_lineups(list_of_matchs)
    columns_with_lineups=get_lineups_columns(game_columns, list_of_lineups, vectors)
    flatten_rows=get_flatten_rows(columns_with_lineups)
    final_df=get_final_df(flatten_rows, vectors)
    return final_df
