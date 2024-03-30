# Synthetic Data Generator

This component includes scripts for generating synthetic data and performing web scraping.

## Usage

To generate synthetic data, follow these steps:

1. Navigate to the `Synthetic Data Generator` directory.
2. Run `main.py` using Python.

### Contents

- `main.py`: Main script to execute data generation.
- `synth_gen`: Python package for data generation.
  - `data`: Directory containing generated data files.
  - `data_generator.py`: Script for generating synthetic data.
  - `web_scraping.py`: Script for web scraping.
  - `__init__.py`: Initialization file.

### Generated Data

The generated tables will be saved as CSV files in the `backend/data` directory:

- `game_attribute.csv`: Contains the generated game attribute data.
- `player_attribute.csv`: Contains the generated player attribute data.
- `player_history.csv`: Contains the generated player history data.

These CSV files can be used for further analysis, modeling, or any other purposes related to the gaming application.

[Back to Main](../README.md)