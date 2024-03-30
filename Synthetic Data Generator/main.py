from synth_gen.data_generator import DataGenerator

def main():
    # Create an instance of the DataGenerator class
    data_generator = DataGenerator()

    # Start the synthetic data generation process with default parameters
    data_generator.start_synthetic_data_generation()

    # Access the generated tables
    game_attributes_table = data_generator.game_attributes_table
    player_attribute_table = data_generator.player_attribute_table
    player_history_table = data_generator.player_history_table

    # Print the generated tables (or perform any other operations you need)
    print("Game Attributes Table:")
    print(game_attributes_table.head())

    print("\nPlayer Attribute Table:")
    print(player_attribute_table.head())

    print("\nPlayer History Table:")
    print(player_history_table.head())

if __name__ == "__main__":
    main()