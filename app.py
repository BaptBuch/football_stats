import streamlit as st
import numpy as np
import pandas as pd
import time

st.set_page_config(layout="wide")

def get_league_seasons():
    st.write('You selected:', option_profil)
    col1, col2 = st.columns([1,1])
    with col1:
        options = st.multiselect('Select a league',['Ligue 1', 'Premier league', 'Championship', 'Liga', 'Bundesliga', 'Serie A', 'Eredevise'])
        st.write('You selected:', ", ".join(options))

        if 'Ligue 1' in options:
            st.image("https://seeklogo.com/images/L/ligue-1-uber-eats-logo-E440240623-seeklogo.com.png",width=100)
        if 'Premier league' in options:
            st.image("https://seeklogo.com/images/P/premier-league-logo-B2889F3974-seeklogo.com.png",width=100)
        if 'Championship' in options:
            st.image("https://seeklogo.com/images/S/sky-bet-championship-logo-C4F6910987-seeklogo.com.png",width=100)
        if 'Liga' in options:
            st.image("https://seeklogo.com/images/L/la-liga-logo-0530344B7E-seeklogo.com.png",width=100)
        if 'Bundesliga' in options:
            st.image("https://seeklogo.com/images/B/bundesliga-logo-CA4C5CF312-seeklogo.com.png",width=100)
        if 'Serie A' in options:
            st.image("https://seeklogo.com/images/S/serie-a-logo-59D3C46AE5-seeklogo.com.png",width=100)
        if 'Eredevise' in options:
            st.image("https://seeklogo.com/images/E/eredivisie-logo-24C3DB32E5-seeklogo.com.png",width=100)
        # se:
        #     st.write('◀️')
    with col2:
        saison = st.radio('Select a saison', ('2015/2016', '2016/2017', '2017/2018', '2018/2019', '2019/2020', '2020/2021'))
    ######################## MENU DEROULANT ############################

    @st.cache

    def get_select_box_data():

        return pd.DataFrame({
            'stats': ["Nombre de remplacant","Minutes jouées / remplacants", "Nombre de blessure", "Retournement de situation", "..." ],
            })

    df = get_select_box_data()

    stats = st.selectbox('Select une stat', df['stats'])


def get_predictions():
    st.markdown("""
    ## Welcome !

    ### Football_stats is not only about stats, but also preds
    We'll **try** to help you build the best tactics for your next games.
    We are working on Machine Learning models build to predict the best possible decisions on substitutions managements for second half of football games.
    """)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.header('1) Information about your team')
        old_rules = st.checkbox('Are you playing in the english Premier League ?', key=100)
        if old_rules:
            new_rules = 'False'
            st.write('New rules : False')
        else:
            new_rules = 'True'

        home_or_away = st.radio("Will you be playing at home or away ?",
        ('Home', 'Away'))
        if home_or_away == "Home":
            agree = st.checkbox('Have you been promoted this year to your current league ?', key=99)
            if agree:
                H_standings = 45
                st.write('Promoted : true')
            else:
                H_standings = st.number_input('How many points did you get last season ?', key=1)
            H_form = st.number_input('What is your position at the start of the game ?', key=38)
            A_standings = st.number_input('How many points did your opponent get last season ?', key=39)
            A_form = st.number_input("What is your opponent's position at the start of the game ?", key=40)
        elif home_or_away == "Away":
            agree = st.checkbox('Have you been promoted this year to your current league ?', key=98)
            if agree:
                A_standings = 45
                st.write('Promoted : true')
            else:
                A_standings = st.number_input('How many points did you get last season ?', key=3)
            A_form = st.number_input('What is your position at the start of the game ?', key=41)
            H_standings = st.number_input('How many points did your opponent get last season ?', key=42)
            H_form = st.number_input("What is your opponent's position at the start of the game ?", key=43)


    with col2:
        st.header('2) Information about your tactics')
        if home_or_away == "Home":
            h_d_start = st.number_input('How many defensive players do you have ?', key=4)
            st.write('The current number of defensive players is ', int(h_d_start))
            Home_D_start = h_d_start

            h_m_start = st.number_input('How many midfield players do you have ?', key=5)
            st.write('The current number of midfield players is ', int(h_m_start))
            Home_M_start = h_m_start

            h_a_start = st.number_input('How many offensive players do you have ?', key=6)
            st.write('The current number of offensive players is ', int(h_a_start))
            Home_A_start = h_a_start
        elif home_or_away == "Away":
            a_d_start = st.number_input('How many defensive players do you have ?', key=7)
            st.write('The current number of defensive players is ', int(a_d_start))
            Away_D_start = a_d_start

            a_m_start = st.number_input('How many midfield players do you have ?', key=8)
            st.write('The current number of midfield players is ', int(a_m_start))
            Away_M_start = a_m_start

            a_a_start = st.number_input('How many offensive players do you have ?', key=9)
            st.write('The current number of offensive players is ', int(a_a_start))
            Away_A_start = a_a_start

        tactic_changes = st.radio("Have you planned to change your lineups at some point in the game ?", ('No','Yes'))
        if tactic_changes == 'Yes':
            if home_or_away == "Home":
                with st.expander("First step: 60'"):
                    st.write("What could be your lineup at 60'? i.e. do you plan to do any changes between 45' and 60'")
                    h_d_60 = st.number_input('How many defensive players ?', key=1110)
                    Home_D_60 = h_d_60

                    h_m_60 = st.number_input('How many midfield players ?', key=1111)
                    Home_M_60 = h_m_60

                    h_a_60 = st.number_input('How many offensive players ?', key=1112)
                    Home_A_60 = h_a_60
                with st.expander("Second step: 75'"):
                    st.write("What could be your lineup at 75'? i.e. do you plan to do any changes between 60' and 75'")
                    h_d_75 = st.number_input('How many defensive players ?', key=1113)
                    Home_D_75 = h_d_75

                    h_m_75 = st.number_input('How many midfield players ?', key=1114)
                    Home_M_75 = h_m_75

                    h_a_75 = st.number_input('How many offensive players ?', key=1115)
                    Home_A_75 = h_a_75
                with st.expander("Final step: 90'"):
                    st.write("What could be your lineup at the end of the game?  i.e. do you plan to do any changes after the 75'")
                    h_d_final = st.number_input('How many defensive players ?', key=116)
                    Home_D_final = h_d_final

                    h_m_final = st.number_input('How many midfield players ?', key=117)
                    Home_M_final = h_m_final

                    h_a_final = st.number_input('How many offensive players ?', key=118)
                    Home_A_final = h_a_final

            if home_or_away == "Away":
                with st.expander("First step: 60'"):
                    st.write("What could be your lineup at 60'? i.e. do you plan to do any changes between 45' and 60'")
                    a_d_60 = st.number_input('How many defensive players ?', key=119)
                    Away_D_60 = a_d_60

                    a_m_60 = st.number_input('How many midfield players ?', key=120)
                    Away_M_60 = a_m_60

                    a_a_60 = st.number_input('How many offensive players ?', key=121)
                    Away_A_60 = a_a_60
                with st.expander("Second step: 75'"):
                    st.write("What could be your lineup at 75'? i.e. do you plan to do any changes between 60' and 75'")
                    a_d_75 = st.number_input('How many defensive players ?', key=122)
                    Away_D_75 = a_d_75

                    a_m_75 = st.number_input('How many midfield players ?', key=123)
                    Away_M_75 = a_m_75

                    a_a_75 = st.number_input('How many offensive players ?', key=124)
                    Away_A_75 = a_a_75
                with st.expander("Final step: 90'"):
                    st.write("What could be your lineup at the end of the game?  i.e. do you plan to do any changes after the 75'")
                    a_d_final = st.number_input('How many defensive players ?', key=125)
                    Away_D_final = a_d_final

                    a_m_final = st.number_input('How many midfield players ?', key=126)
                    Away_M_final = a_m_final

                    a_a_final = st.number_input('How many offensive players ?', key=127)
                    Away_A_final = a_a_final


        else:
            if home_or_away == "Home":
                Home_D_60, Home_M_60, Home_A_60 = Home_D_75, Home_M_75, Home_A_75 = Home_D_final, Home_M_final, Home_A_final = Home_D_start, Home_M_start, Home_A_start
            elif home_or_away == "Away":
                Away_D_60, Away_M_60, Away_A_60 = Away_D_75, Away_M_75, Away_A_75 = Away_D_final, Away_M_final, Away_A_final = Away_D_start, Away_M_start, Away_A_start

    with col3:
        st.header('3) Information about your opponent')
        if home_or_away == "Home":
            a_d_start = st.number_input('How many defensive players do you think your opponent will play with ?', key=28)
            st.write('The current number of defensive players is ', int(a_d_start))
            Home_D_start = a_d_start

            a_m_start = st.number_input('How many midfield players do you think your opponent will play with ?', key=29)
            st.write('The current number of midfield players is ', int(a_m_start))
            Home_M_start = a_m_start

            a_a_start = st.number_input('How many offensive players do you think your opponent will play with ?', key=30)
            st.write('The current number of offensive players is ', int(a_a_start))
            Home_A_start = a_a_start
        elif home_or_away == "Away":
            a_d_start = st.number_input('How many defensive players do you think your opponent will play with ?', key=33)
            st.write('The current number of defensive players is ', int(a_d_start))
            Away_D_start = a_d_start

            a_m_start = st.number_input('How many midfield players do you think your opponent will play with ?', key=34)
            st.write('The current number of midfield players is ', int(a_m_start))
            Away_M_start = a_m_start

            a_a_start = st.number_input('How many offensive players do you think your opponent will play with ?', key=35)
            st.write('The current number of offensive players is ', int(a_a_start))
            Away_A_start = a_a_start

        tactic_changes = st.radio("Do you know if your opponent is used to do some tactical changes at some point in the game ?", ('No','Yes'))
        if tactic_changes == 'Yes':
            if home_or_away == "Home":
                with st.expander("First step: 60'"):
                    st.write("What could be their lineup at 60'?")
                    h_d_60 = st.number_input('How many defensive players ?', key=10)
                    Home_D_60 = h_d_60

                    h_m_60 = st.number_input('How many midfield players ?', key=11)
                    Home_M_60 = h_m_60

                    h_a_60 = st.number_input('How many offensive players ?', key=12)
                    Home_A_60 = h_a_60
                with st.expander("Second step: 75'"):
                    st.write("What could be their lineup at 75'?")
                    h_d_75 = st.number_input('How many defensive players ?', key=13)
                    Home_D_75 = h_d_75

                    h_m_75 = st.number_input('How many midfield players ?', key=14)
                    Home_M_75 = h_m_75

                    h_a_75 = st.number_input('How many offensive players ?', key=15)
                    Home_A_75 = h_a_75
                with st.expander("Final step: 90'"):
                    st.write("What could be their lineup at end time?")
                    h_d_final = st.number_input('How many defensive players ?', key=16)
                    Home_D_final = h_d_final

                    h_m_final = st.number_input('How many midfield players ?', key=17)
                    Home_M_final = h_m_final

                    h_a_final = st.number_input('How many offensive players ?', key=18)
                    Home_A_final = h_a_final

            if home_or_away == "Away":
                with st.expander("First step: 60'"):
                    st.write("What could be their lineup at 60'?")
                    a_d_60 = st.number_input('How many defensive players ?', key=19)
                    Away_D_60 = a_d_60

                    a_m_60 = st.number_input('How many midfield players ?', key=20)
                    Away_M_60 = a_m_60

                    a_a_60 = st.number_input('How many offensive players ?', key=21)
                    Away_A_60 = a_a_60
                with st.expander("Second step: 75'"):
                    st.write("What could be their lineup at 75'?")
                    a_d_75 = st.number_input('How many defensive players ?', key=22)
                    Away_D_75 = a_d_75

                    a_m_75 = st.number_input('How many midfield players ?', key=23)
                    Away_M_75 = a_m_75

                    a_a_75 = st.number_input('How many offensive players ?', key=24)
                    Away_A_75 = a_a_75
                with st.expander("Final step: 90'"):
                    st.write("What could be their lineup at end time?")
                    a_d_final = st.number_input('How many defensive players ?', key=25)
                    Away_D_final = a_d_final

                    a_m_final = st.number_input('How many midfield players ?', key=26)
                    Away_M_final = a_m_final

                    a_a_final = st.number_input('How many offensive players ?', key=27)
                    Away_A_final = a_a_final


        else:
            if home_or_away == "Home":
                Home_D_60, Home_M_60, Home_A_60 = Home_D_75, Home_M_75, Home_A_75 = Home_D_final, Home_M_final, Home_A_final = Home_D_start, Home_M_start, Home_A_start
            elif home_or_away == "Away":
                Away_D_60, Away_M_60, Away_A_60 = Away_D_75, Away_M_75, Away_A_75 = Away_D_final, Away_M_final, Away_A_final = Away_D_start, Away_M_start, Away_A_start


    with col4:
        st.header('4) Information about your game')
        if home_or_away == "Home":
            st.write("What's the score at half time ?")
            h_goals_ht = st.number_input('How many goals did you score ?', key=31)
            a_goals_ht = st.number_input('How many goals did your opponent score ?', key=32)
            score_ht = f'[{h_goals_ht}, {a_goals_ht}]'
            if h_goals_ht > a_goals_ht:
                result_ht = 'H'
            elif a_goals_ht > h_goals_ht:
                result_ht = 'A'
            else:
                result_ht = 'D'
            h_ht_changes = st.checkbox('Did you do substitutions before or at half time ?', key=97)
            if h_ht_changes:
                st.write("What is your time?")
                h_d_ht = st.number_input('How many defensive players ?', key=44)
                Home_D_ht = h_d_ht
                h_m_ht = st.number_input('How many midfield players ?', key=45)
                Home_M_ht = h_m_ht
                h_a_ht = st.number_input('How many offensive players ?', key=46)
                Home_A_ht = h_a_ht
            a_ht_changes = st.checkbox('Did your opponent do substitutions before or at half time ?', key=96)
            if a_ht_changes:
                a_d_ht = st.number_input('How many defensive players ?', key=47)
                Away_D_ht = a_d_ht
                a_m_ht = st.number_input('How many midfield players ?', key=48)
                Away_M_ht = a_m_ht
                a_a_ht = st.number_input('How many offensive players ?', key=49)
                Away_A_ht = a_a_ht

        elif home_or_away == "Away":
            st.write("What's the score at half time ?")
            a_goals_ht = st.number_input('How many goals did you score ?', key=36)
            h_goals_ht = st.number_input('How many goals did your opponent score ?', key=37)
            score_ht = f'[{h_goals_ht}, {a_goals_ht}]'
            if h_goals_ht > a_goals_ht:
                result_ht = 'H'
            elif a_goals_ht > h_goals_ht:
                result_ht = 'A'
            else:
                result_ht = 'D'
            h_ht_changes = st.checkbox('Did your opponent do substitutions before or at half time ?', key=97)
            if h_ht_changes:
                h_d_ht = st.number_input('How many defensive players ?', key=44)
                Home_D_ht = h_d_ht
                h_m_ht = st.number_input('How many midfield players ?', key=45)
                Home_M_ht = h_m_ht
                h_a_ht = st.number_input('How many offensive players ?', key=46)
                Home_A_ht = h_a_ht
            a_ht_changes = st.checkbox('Did you do substitutions before or at half time ?', key=96)
            if a_ht_changes:
                a_d_ht = st.number_input('How many defensive players ?', key=47)
                Away_D_ht = a_d_ht
                a_m_ht = st.number_input('How many midfield players ?', key=48)
                Away_M_ht = a_m_ht
                a_a_ht = st.number_input('How many offensive players ?', key=49)
                Away_A_ht = a_a_ht

    if st.checkbox('Show progress bar', key=95):
        'Starting a long computation...'

        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)
        columns = ['result_ht','Home_D_start',
       'Home_M_start', 'Home_A_start', 'Away_D_start', 'Away_M_start',
       'Away_A_start', 'Home_D_ht', 'Home_M_ht', 'Home_A_ht', 'Away_D_ht',
       'Away_M_ht', 'Away_A_ht', 'Home_D_60', 'Home_M_60', 'Home_A_60',
       'Away_D_60', 'Away_M_60', 'Away_A_60', 'Home_D_75', 'Home_M_75',
       'Home_A_75', 'Away_D_75', 'Away_M_75', 'Away_A_75', 'Home_D_final',
       'Home_M_final', 'Home_A_final', 'Away_D_final', 'Away_M_final',
       'Away_A_final']
        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f'{i+1} % done')
            bar.progress(i + 1)
            time.sleep(0.1)
        y = [result_ht,Home_D_start,
            Home_M_start, Home_A_start, Away_D_start, Away_M_start,
            Away_A_start, Home_D_ht, Home_M_ht, Home_A_ht, Away_D_ht,
            Away_M_ht, Away_A_ht, Home_D_60, Home_M_60, Home_A_60,
            Away_D_60, Away_M_60, Away_A_60, Home_D_75, Home_M_75,
            Home_A_75, Away_D_75, Away_M_75, Away_A_75, Home_D_final,
            Home_M_final, Home_A_final, Away_D_final, Away_M_final,
            Away_A_final]
        result_dictionary = dict(zip(columns, y))
        '...and now we\'re done!'

        ## ==>> HERE PRINT THE PREDICT OF OUR API


#######################IMAGE EN BACKGROUND###########################

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.write("")

with col2:
    st.image("https://image.freepik.com/vecteurs-libre/silhouette-footballeurs-autour-ballon-football-fond-blanc_1302-10553.jpg", width=400)

with col3:
    st.write("")

#######################Sélection du profil###########################

option_profil = st.selectbox(
    "Why are you here ?",
   ('','For the stats !', 'For the predictions !'))


######################## BOX lEAGUE SAISON ############################
if option_profil == 'For the stats !':
    get_league_seasons()

##################### BOX lEAGUE PREDICTIONS #########################
if option_profil == 'For the predictions !':
    get_predictions()
