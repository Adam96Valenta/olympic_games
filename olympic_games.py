import streamlit as st
import pandas as pd
import numpy as np
import altair as alt


olympic_games = pd.read_csv('olympic_medals.csv')
olympic_names = pd.read_csv('olympic_hosts.csv')

olympic_games = olympic_games[['discipline_title', 'slug_game', 'event_title', 'event_gender', 'medal_type', 'participant_type','athlete_full_name' , 'country_name', 'country_3_letter_code']]
olympic_games['athlete_full_name'] = olympic_games['athlete_full_name'].replace(np.nan, 'Team')

olympic_names.drop(columns=['game_end_date', 'game_start_date'], inplace=True)
olympic_names.rename(columns={'game_slug':'slug_game'}, inplace=True)

df = pd.merge(olympic_games,olympic_names, how='left', on= 'slug_game')
df['Gold'] = np.where(df['medal_type'] == 'GOLD', 1, 0)
df['Silver'] = np.where(df['medal_type'] == 'SILVER', 1, 0)
df['Bronze'] = np.where(df['medal_type'] == 'BRONZE', 1, 0)
df['Total'] = 1
df['rank'] = np.where(df.loc[:,'medal_type'] == 'GOLD', 1, np.where(df.loc[:,'medal_type'] == 'SILVER',2,3))
df = df[['game_name', 'game_location','game_season', 'game_year', 'discipline_title','event_title', 'event_gender', 'athlete_full_name', 'country_name', 'country_3_letter_code', 'medal_type','Gold', 'Silver', 'Bronze', 'Total', 'rank']]
df = df.drop_duplicates()


st.markdown('# Olympic Summer & Winter Games, 1896-2022')

c1, c2 = st.columns(2)

c1.image('./olympic_games.png')

c2.subheader(f'Hello!')
c2.write(f"""
Welcome in my first Streamlit app.\n
In this application you can find results from all the Olympic Games from 1896 to 2022. \n
If you're on a mobile device,  I would recommend  switch over to landscape for viewing ease. \n
I worked with datasets from [Kaggle.com](https://www.kaggle.com/code/kalilurrahman/olympic-games-eda). \n
You can find the source code [here](https://github.com/Adam96Valenta/olympic_games).
    """)



with st.container():
    name_choice = st.selectbox('Choose name of Olympic Games:', df['game_name'].unique())

    df = df[df['game_name'] == name_choice]

    c1, c2 = st.columns(2)

    with c1:
        df_country = df.groupby('country_name')[['Gold', 'Silver', 'Bronze', 'Total']].sum().sort_values(
            by=['Total', 'Gold', 'Silver'], ascending=False).reset_index()


        st.write(df_country)


    with c2:
        df_athlete = df.query('athlete_full_name != "Team"').groupby('athlete_full_name')[
            ['Gold', 'Silver', 'Bronze', 'Total']].sum().sort_values(by=['Total', 'Gold', 'Silver'],
                                                                         ascending=False).reset_index()

        st.write(df_athlete)

    with st.container():
        st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

        medal = st.radio('Choose type of medal:', ['GOLD', 'SILVER', 'BRONZE'])
        if medal == 'GOLD':
            df_country = df.groupby('country_name')['Gold'].sum().reset_index().sort_values(by=['Gold'], ascending=False).head(30)

            chart = alt.Chart(df_country).mark_bar().encode(
                y='Gold',
                x=alt.X('country_name:N', sort='-y'),
            ).properties(
                height=500
            ).configure_mark(
                color='gold'
            ).configure_axisX(
                labelAngle=-45
            )
            st.altair_chart(chart, use_container_width=True)

        elif medal == 'SILVER':
            df_country = df.groupby('country_name')['Silver'].sum().reset_index().sort_values(by=['Silver'], ascending=False).head(30)

            chart = alt.Chart(df_country).mark_bar().encode(
                y='Silver',
                x=alt.X('country_name:N', sort='-y'),
            ).properties(
                 height=500
            ).configure_mark(
                color='silver'
            ).configure_axisX(
                labelAngle=-45
            )
            st.altair_chart(chart, use_container_width=True)

        elif medal == 'BRONZE':
            df_country = df.groupby('country_name')['Bronze'].sum().reset_index().sort_values(by=['Bronze'], ascending=False).head(30)

            chart = alt.Chart(df_country).mark_bar().encode(
                y='Bronze',
                x=alt.X('country_name:N', sort='-y'),
            ).properties(
                height=500
            ).configure_mark(
                color='#cd7f32'
            ).configure_axisX(
                labelAngle=-45
            )
            st.altair_chart(chart, use_container_width=True)

c1, c2 = st.columns(2)

with c1:

    discipline_title = st.selectbox('Choose discipline:', df['discipline_title'].unique())
    event_title = st.selectbox('Choose event:', df[(df['discipline_title'] == discipline_title)]['event_title'].unique())

    df1 = df[(df['discipline_title'] == discipline_title) & (df['event_title'] == event_title)]
    if ('Team' in df1['athlete_full_name'].to_list()) == True:
        df1 = df1[['country_name', 'country_3_letter_code', 'medal_type', 'rank']].sort_values(
            by=['rank']).set_index('rank')
    else:
        df1 = df1[['athlete_full_name', 'country_3_letter_code', 'medal_type', 'rank']].sort_values(
            by=['rank']).set_index('rank')
    st.write(df1)

with c2:
    country_name = st.selectbox('Choose country name:', df['country_name'].unique())

    df2 = df[df['country_name'] == country_name]
    df2 = df2.groupby('discipline_title')[['Gold','Silver','Bronze','Total']].sum().sort_values(
            by=['Total', 'Gold', 'Silver'], ascending=False).reset_index()
    st.write(df2)

