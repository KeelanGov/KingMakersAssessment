from flask import Flask, jsonify
import mysql.connector
from pymongo import MongoClient
import pandas as pd
import numpy as np

app = Flask(__name__)

# Database connection details
db_config_mysql = {
    'host': 'db',
    'user': 'root',
    'password': 'secret',
    'database': 'games_db'
}

# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client['game_recommendation']
item_neighborhoods = db['item_neighborhoods']

def get_player_top_games(player_id, player_history_df, top_n=5):
    player_games = player_history_df[player_history_df['player_id'] == player_id]
    player_top_games = player_games['game_id'].value_counts().head(top_n).index.tolist()
    return player_top_games

def get_recommended_games(player_id, num_recommendations, player_history_df, item_neighborhoods):
    # Get the player's top played games from MongoDB
    top_games = get_player_top_games(player_id, player_history_df)
    
    # Get similar games for each top game from MongoDB
    similar_games = set()
    for game_id in top_games:
        similar_games.update(item_neighborhoods.find_one({'_id': game_id})['neighbors'])
    
    # Remove games already played by the player
    played_games = player_history_df[player_history_df['player_id'] == player_id]['game_id'].unique()
    recommended_games = list(similar_games - set(played_games))
    
    # Return the top recommended games
    return recommended_games[:num_recommendations]

@app.route('/recommendations/<int:player_id>')
def get_recommendations(player_id):
    # Connect to the MySQL database
    conn_mysql = mysql.connector.connect(**db_config_mysql)
    cursor_mysql = conn_mysql.cursor()

    # Fetch player history from MySQL
    query_player_history = """
    SELECT player_id, game_id
    FROM player_history
    """
    cursor_mysql.execute(query_player_history)
    player_history_data = cursor_mysql.fetchall()
    player_history_df = pd.DataFrame(player_history_data, columns=['player_id', 'game_id'])

    # Close MySQL connection
    cursor_mysql.close()
    conn_mysql.close()

    # Get recommendations using MongoDB and player history
    num_recommendations = 10
    recommended_games = get_recommended_games(player_id, num_recommendations, player_history_df, item_neighborhoods)

    return jsonify(recommended_games)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
