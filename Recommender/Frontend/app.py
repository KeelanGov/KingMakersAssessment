import streamlit as st
import requests
import pandas as pd

api_url = 'http://api:5000'

def get_player_info(player_id):
    response = requests.get(f'{api_url}/player/{player_id}')
    player_info = response.json()
    return player_info

def get_recommendations(player_id):
    response = requests.get(f'{api_url}/recommendations/{player_id}')
    recommendations = response.json()
    return recommendations

def get_game_info(game_ids):
    response = requests.post(f'{api_url}/games', json={'game_ids': game_ids})
    game_info = response.json()
    return game_info

st.set_page_config(page_title='Game Recommender', layout='wide')

st.title('Game Recommender')

player_id = st.number_input('Enter Player ID', min_value=1, step=1)

if st.button('Get Recommendations'):
    player_info = get_player_info(player_id)
    recommendations = get_recommendations(player_id)
    game_info = get_game_info(recommendations)

    st.subheader('Player Information')
    st.write(f"Name: {player_info['first_name']} {player_info['last_name']}")

    st.subheader('Recommended Games')
    recommended_games_df = pd.DataFrame(game_info, columns=['game_id', 'game_name'])
    st.table(recommended_games_df)