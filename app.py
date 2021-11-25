import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")

#######################IMAGE EN BACKGROUND###########################

col1, col2, col3 = st.columns([1,1,1])

with col1:
    st.write("")

with col2:
    st.image("https://image.freepik.com/vecteurs-libre/silhouette-footballeurs-autour-ballon-football-fond-blanc_1302-10553.jpg")

with col3:
    st.write("")



######################## BOX lEAGUE SAISON ############################

col1, col2 = st.columns([1,1])

with col1:

    league = st.radio('Select a league', ('Ligue 1', 'Premier league', 'Champion Ship', 'Liga', 'Bundesliga', 'Serie A', 'Eredevise'))

    if league == 'Ligue 1':
        st.image("https://seeklogo.com/images/L/ligue-1-uber-eats-logo-E440240623-seeklogo.com.png",width=100)
    elif league == 'Premier league':
        st.image("https://seeklogo.com/images/P/premier-league-logo-B2889F3974-seeklogo.com.png",width=100)
    elif league == 'Champion Ship':
        st.image("https://seeklogo.com/images/S/sky-bet-championship-logo-C4F6910987-seeklogo.com.png",width=100)
    elif league == 'Liga':
        st.image("https://seeklogo.com/images/L/la-liga-logo-0530344B7E-seeklogo.com.png",width=100)
    elif league == 'Bundesliga':
        st.image("https://seeklogo.com/images/B/bundesliga-logo-CA4C5CF312-seeklogo.com.png",width=100)
    elif league == 'Serie A':
        st.image("https://seeklogo.com/images/S/serie-a-logo-59D3C46AE5-seeklogo.com.png",width=100)
    elif league == 'Eredevise':
        st.image("https://seeklogo.com/images/E/eredivisie-logo-24C3DB32E5-seeklogo.com.png",width=100)
    else:
        st.write('◀️')

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
