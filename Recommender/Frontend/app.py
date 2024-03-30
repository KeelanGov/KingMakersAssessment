import streamlit as st
import requests

api_url = 'http://api:5001'

def get_recommendations(player_id):
    response = requests.get(f'{api_url}/recommendations/{player_id}')
    recommendations = response.json()
    return recommendations

st.title('Game Recommender')

player_id = st.number_input('Enter Player ID', min_value=1, step=1)

if st.button('Get Recommendations'):
    recommendations = get_recommendations(player_id)
    st.subheader('Recommended Games')
    for game_id in recommendations:
        st.write(f'- Game ID: {game_id}')