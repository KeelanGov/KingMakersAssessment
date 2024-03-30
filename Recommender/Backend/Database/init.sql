USE games_db;

CREATE TABLE game_attributes (
    game_id INT PRIMARY KEY,
    game_name VARCHAR(255),
    wild_symbols VARCHAR(255),
    scatter_symbols VARCHAR(255),
    free_spins INT,
    bonus_rounds VARCHAR(255),
    multipliers VARCHAR(255),
    jackpots VARCHAR(255),
    paylines INT,
    reel_mechanisms VARCHAR(255),
    gamble_feature VARCHAR(255),
    rtp FLOAT,
    volatility VARCHAR(255),
    themes VARCHAR(255),
    mystery_symbols VARCHAR(255),
    random_triggers VARCHAR(255)
);

CREATE TABLE player_attributes (
    player_id INT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

CREATE TABLE player_history (
    player_id INT,
    game_id INT
);

LOAD DATA INFILE '/var/lib/mysql-files/game_attribute.csv' INTO TABLE game_attributes
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/player_attribute.csv' INTO TABLE player_attributes
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/player_history.csv' INTO TABLE player_history
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;