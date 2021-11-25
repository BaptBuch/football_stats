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

    If you want to try, we'll need you to give us some data on your team and tactics.
""")

    old_rules = st.checkbox('Are you playing in the english Premier League ?')
    if old_rules:
        new_rules = 'False'
        st.write('Old rules : true')
    else:
        new_rules = 'True'

    home_or_away = st.radio("Will you be playing at home or away ?",
     ('Home', 'Away'))
    if home_or_away == "Home":
        agree = st.checkbox('Have you been promoted this year to your current league ?')
        if agree:
            H_standings = 45
            st.write('Promoted : true')
        else:
            standings = st.number_input('How many points did you get last season ?')
            H_standings = standings

        number = st.number_input('How many defensive players do you have ?')
        st.write('The current number of defensive players is ', int(number))
        Home_D_start = number

        number = st.number_input('How many midfield players do you have ?')
        st.write('The current number of midfield players is ', int(number))
        Home_M_start = number

        number = st.number_input('How many offensive players do you have ?')
        st.write('The current number of offensive players is ', int(number))
        Home_A_start = number

        radio_result_ht = st.radio("What's your result at half-time ?",
        ('Win', 'Draw', 'Loose'))
        if radio_result_ht == 'Win':
            result_ht = "H"
        elif radio_result_ht == "Loose":
            result_ht = 'A'
        else:
            result_ht = "D"
    if home_or_away == "Away":
        agree = st.checkbox('Have you been promoted this year to your current league ?')
        if agree:
            A_standings = 45
            st.write('Promoted : true')
        else:
            standings = st.number_input('How many points did you get last season ?')
            A_standings = standings

        number = st.number_input('How many defensive players do you have ?')
        st.write('The current number of defensive players is ', int(number))
        Away_D_start = number

        number = st.number_input('How many midfield players do you have ?')
        st.write('The current number of midfield players is ', int(number))
        Away_M_start = number

        number = st.number_input('How many offensive players do you have ?')
        st.write('The current number of offensive players is ', int(number))
        Away_A_start = number

        radio_result_ht = st.radio("What's your result at half-time ?",
        ('Win', 'Draw', 'Loose'))
        if radio_result_ht == 'Win':
            result_ht = "A"
        elif radio_result_ht == "Loose":
            result_ht = 'H'
        else:
            result_ht = "D"




    if st.checkbox('Show progress bar'):
        'Starting a long computation...'

        # Add a placeholder
        latest_iteration = st.empty()
        bar = st.progress(0)

        for i in range(100):
            # Update the progress bar with each iteration.
            latest_iteration.text(f'{i+1} % done')
            bar.progress(i + 1)
            time.sleep(0.1)
        if home_or_away == "Home":
            print(new_rules, result_ht, Home_D_start, Home_M_start, Home_M_start)
        elif home_or_away == "Away":
            print(new_rules, result_ht, Away_D_start, Away_M_start, Away_M_start)
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
