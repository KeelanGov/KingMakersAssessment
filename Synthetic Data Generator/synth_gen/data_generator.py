from .web_scraping import scrape_first_site, scrape_second_site, scrape_third_site
import logging
import random
import pandas as pd
import csv
import names
import numpy as np
import os
import pickle

logger = logging.Logger(__name__)
logger.setLevel(logging.INFO)

class DataGenerator:
    """
    Data generator class for synthetic data generation
    Creates tables:
        - Game Attributes
        - Player Attributes
        - Player History
    
    Also holds metadata on game attributes.
    """
    def __init__(self):
        """"
        game_attributes_metadata: Metadata on game attributes (expected values) or datatypes
        game_attributes_table: Attributes on the games being played - must adhere to expected metadata
        player_attributes_table: Attributes on players. Currently: player_id, first_name and last_name
        player_history_table: Represents players game history, i.e. All games they've played and their respective metadata.
        """
        self.game_attributes_metadata = {
            "game_id": int, 
            "game_name": str, 
            "wild_symbols": ["regular", "expanding", "sticky"], 
            "scatter_symbols": ["yes", "no"], 
            "free_spins": int, 
            "bonus_rounds": ["yes", "no"], 
            "multipliers": int,
            "jackpots": ["fixed", "progressive"], 
            "paylines": int, 
            "reel_mechanisms": ["cascading", "megaways"], 
            "gamble_feature": ["yes", "no"], 
            "rtp": float, 
            "volatility": ["high", "medium", "low"], 
            "themes": str,
            "mystery_symbols": ["yes", "no"], 
            "random_triggers": ["yes", "no"] 
        }
        self.game_attributes_table = None
        self.player_attribute_table = None
        self.player_history_table = None

        def read_external_data(self, file_path, type):
            """
            Reads in an external dataset, of type:
            - game_attribute: will continue with steps after game_attribute_table
            - player_attribute: will continue with steps after player_attribute_table population
            - player_history: no continuation, just reads in table

            Should possibly move to a DataLoader class...
            """
            raise NotImplementedError("This process has not been implemented yet.")
            if type == "game_attribute":
                self._check_game_attribute_table(file_path)
                self.start_synthetic_data_generation(override=type)
            elif type == "player_attribute":
                self._check_player_attribute_table(file_path)
                self.start_synthetic_data_generation(override=type)
            elif type == "player_history":
                self.check_player_history_table(file_path)
            else:
                print("Invalid data type specified.")
                

    def start_synthetic_data_generation(self, num_rows=1000, num_players=200, max_games_played=30, override=None):
        """
        This function kicks off the synthetic data generation
        Parameters:
        -----------
        num_rows: Set to 1000 by default - represents number of rows/games in the game attribute table
        num_players: Set to 200 by default - represents number of players who've played
        overrride_game_attributes: If True, skips the populate_game_attributes_table step
        overrride_player_attributes: If True, skips the populate_player_attribute_table step
        """
        if  override == "player_attribute":
            raise NotImplementedError("This process has not been implemented yet.")
            self.game_attributes_table = self.populate_game_attributes_table(num_rows)
            self.player_history_table = self.populate_player_history_table(max_games_played)

        elif override == "game_attribute":
            raise NotImplementedError("This process has not been implemented yet.")
            self.player_attribute_table = self.populate_player_attribute_table(num_players)
            self.player_history_table = self.populate_player_history_table(max_games_played)

        elif not override:
            self.game_attributes_table = self.populate_game_attributes_table(num_rows)
            self.player_attribute_table = self.populate_player_attribute_table(num_players)
            self.player_history_table = self.populate_player_history_table(max_games_played)

        self.game_attributes_table.to_csv(f'synth_gen/data/game_attribute.csv', index=False)
        self.player_attribute_table.to_csv(f'synth_gen/data/player_attribute.csv', index=False)
        self.player_history_table.to_csv(f'synth_gen/data/player_history.csv', index=False)

    def populate_game_attributes_table(self, num_rows):
        """
        The first step in the synthetic data generation is to populate the 
        game attributes table.
        num_rows: Number of games and metadata to populate
        """
        logger.info("Starting to gather data for player names")
        game_names_list = self.get_game_names()

        logger.info("Populating Game Attribute Table with synthetic data")
        game_attribute_data = []
        for i in range(num_rows):
            game_id = i+1
            game_name = game_names_list[i]
            wild_symbols_type = random.choice(["Regular", "Expanding", "Sticky"])
            scatter_symbols_presence = random.choice(["Yes", "No"])
            free_spins_count = random.randint(0, 50)
            bonus_rounds_presence = random.choice(["Yes", "No"])
            multiplier_value = random.randint(2, 10)
            jackpot_type = random.choice(["Progressive"])
            paylines_count = random.randint(0, 50)
            reel_mechanism_type = random.choice(["Cascading", "Megaways"])
            gamble_feature_presence = random.choice(["Yes", "No"])
            rtp_percentage = round(random.uniform(1, 99), 2)
            volatility_level = random.choice(["High", "Low"])
            theme_type = random.choice([
                "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary", "Drama",
                "Family","Fantasy","Film Noir","History","Horror","Music","Musical","Mystery","Romance","Sci-Fi",
                "Sport","Thriller","War","Western"])
            mystery_symbols_presence = random.choice(["Yes", "No"])
            random_triggers_presence = random.choice(["Yes", "No"])

            game_attribute_row = [
                game_id, 
                game_name, 
                wild_symbols_type, 
                scatter_symbols_presence, 
                free_spins_count,
                bonus_rounds_presence, 
                multiplier_value, 
                jackpot_type, 
                paylines_count, 
                reel_mechanism_type,
                gamble_feature_presence, 
                rtp_percentage, 
                volatility_level, 
                theme_type, 
                mystery_symbols_presence,
                random_triggers_presence
            ]
            game_attribute_data.append(game_attribute_row)

        game_attribute_columns = [
            "game_id", "game_name", "wild_symbols", "scatter_symbols", "free_spins", "bonus_rounds", "multipliers",
            "jackpots", "paylines", "reel_mechanisms", "gamble_feature", "rtp", "volatility", "themes",
            "mystery_symbols", "random_triggers"
        ]

        return pd.DataFrame(game_attribute_data, columns=game_attribute_columns)
        
    def populate_player_attribute_table(self, num_players=200):
        """
        The second step in the synthetic data generation is to populate the 
        player attributes table.
        num_players: Number of players in the dataset
        """
        player_attribute_data = []
        player_attribute_data.extend([player_id, names.get_first_name(), names.get_last_name()] for player_id in range(num_players))
        return pd.DataFrame(player_attribute_data, columns=['player_id', 'first_name', 'last_name'])
    
    def populate_player_history_table(self, max_games_played, same_machine_probability=0.7):
        """
        The last step in the synthetic data generation is to populate the player history table.
        max_games_played: Max number of games a player can play.
        same_machine_probability: Probability of a player using the same machine for the next game.
        """
        player_history_data = []
        max_number_of_games_played = max_games_played

        for player_id in range(len(self.player_attribute_table)):
            num_games_played = np.random.randint(0, max_number_of_games_played + 1)
            games_played = []

            # Choose the first game randomly
            game_id = np.random.choice(self.game_attributes_table['game_id'].values)
            games_played.append(game_id)

            for _ in range(num_games_played - 1):
                if np.random.random() < same_machine_probability:
                    # Player uses the same machine for the next game
                    games_played.append(game_id)
                else:
                    # Player switches to a different machine for the next game
                    game_id = np.random.choice(self.game_attributes_table['game_id'].values)
                    games_played.append(game_id)

            player_history_data.extend([[player_id, game_id] for game_id in games_played])

        return pd.DataFrame(player_history_data, columns=['player_id', 'game_id'])


    def get_game_names(self):
        """
        Utilizes the web_scraping module to retrieve
        game names for populating the Game Attribute Table
        """
        if os.path.exists("synth_gen/data/web_scraping_cache.pkl"):
            with open("synth_gen/data/web_scraping_cache.pkl", 'rb') as f:
                game_name_list = pickle.load(f)
            logger.info(f"Loaded {len(game_name_list)} cached game names from web_scraping_cache.pkl")
        else:
            game_names_1 = scrape_first_site()
            game_names_2 = scrape_second_site()
            game_names_3 = scrape_third_site()
            game_name_list = list(set(game_names_1).union(game_names_2).union(game_names_3))
            # randomize to shuffle game names around
            random.shuffle(game_name_list)
            with open("synth_gen/data/web_scraping_cache.pkl", 'wb') as f:
                pickle.dump(game_name_list, f)
            logger.info("Game names retrieved")

        return game_name_list
    
        def _check_game_attribute_table(self, file_path):
            """
            
            """
            raise NotImplementedError("This process has not been implemented yet.")
            try:
                with open(file_path, 'r') as file:
                    reader = csv.DictReader(file)
                    columns = reader.fieldnames

                    # Check if all metadata fields are present in the CSV columns
                    metadata_fields = set(self.game_attributes_metadata.keys())
                    if not metadata_fields.issubset(set(columns)):
                        missing_fields = metadata_fields.difference(set(columns))
                        print(f"Warning: Missing fields in CSV: {', '.join(missing_fields)}")

                    # Check if there are any extra columns not present in the metadata
                    extra_columns = set(columns).difference(metadata_fields)
                    if extra_columns:
                        print(f"Warning: Extra columns in CSV: {', '.join(extra_columns)}")

                    # Read the data from the CSV
                    data = list(reader)
                    self.game_attributes_table.extend(data)

            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found.")
            except Exception as e:
                print(f"Error: {str(e)}")

        def _check_player_attribute_table(self, file_path):
            """
            """
            raise NotImplementedError("This process has not been implemented yet.")

        def check_player_history_table(self, file_path):
            """
            """
            raise NotImplementedError("This process has not been implemented yet.")