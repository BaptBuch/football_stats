import matplotlib.pyplot as plt
#import numpy as np
import pandas as pd
#import plotly.graph_objects as go
import os

token = os.getenv('API_TOKEN')
league_ids =[301,82,564,384,8,9,72]


def filter_df_league(df, league_ids):
    my_df = pd.DataFrame()
    for league_id in league_ids:
        my_df = pd.concat([my_df, df[df.league_id == league_id]])
    return my_df


def count_plot_goals(league_ids=league_ids):
    main_df=pd.read_csv("football_stats/data/df_to_use/stats_df.csv")
    df_games_filtred = filter_df_league(main_df, league_ids).reset_index()
    nb_of_games = len(df_games_filtred.game_id)
    list_nb_goals = []
    total_nb_goals = 0
    for i in range(nb_of_games):
        nb_goals = df_games_filtred.loc[
            i, "ft_score_local"] + df_games_filtred.loc[i, "ft_score_vis"]
        list_nb_goals.append(nb_goals)
        total_nb_goals += nb_goals
    df_nb_of_goals = pd.DataFrame()
    df_nb_of_goals["x"] = list_nb_goals
    df_nb_of_goals["y"] = 0
    y = [0, 0, 0, 0, 0, 0, 0, 0]
    for idx in range(len(df_nb_of_goals["x"])):
        if df_nb_of_goals.loc[idx, "x"] == 0:
            y[0] += 1
            df_nb_of_goals.loc[idx, "y"] = y[0]
        elif df_nb_of_goals.loc[idx, "x"] == 1:
            y[1] += 1
            df_nb_of_goals.loc[idx, "y"] = y[1]
        elif df_nb_of_goals.loc[idx, "x"] == 2:
            y[2] += 1
            df_nb_of_goals.loc[idx, "y"] = y[2]
        elif df_nb_of_goals.loc[idx, "x"] == 3:
            y[3] += 1
            df_nb_of_goals.loc[idx, "y"] = y[3]
        elif df_nb_of_goals.loc[idx, "x"] == 4:
            y[4] += 1
            df_nb_of_goals.loc[idx, "y"] = y[4]
        elif df_nb_of_goals.loc[idx, "x"] == 5:
            y[5] += 1
            df_nb_of_goals.loc[idx, "y"] = y[5]
        elif df_nb_of_goals.loc[idx, "x"] == 6:
            y[6] += 1
            df_nb_of_goals.loc[idx, "y"] = y[6]
        else:
            y[7] += 1
            df_nb_of_goals.loc[idx, "y"] = y[7]

    print(f"The average number of goals is: {sum(list_nb_goals)/nb_of_games}")
    plt.bar(df_nb_of_goals["x"], df_nb_of_goals["y"])
    plt.xlabel('nb of goals')
    plt.ylabel('nb of games')
    plt.show()


count_plot_goals()
