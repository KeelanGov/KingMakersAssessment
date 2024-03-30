# Use an appropriate database image as the base image
FROM mysql:8.0

# Set environment variables for database configuration
ENV MYSQL_DATABASE games_db
ENV MYSQL_ROOT_PASSWORD secret

# Copy database initialization scripts and CSV files
COPY init.sql /docker-entrypoint-initdb.d/
COPY Data/game_attribute.csv /var/lib/mysql-files/
COPY Data/player_attribute.csv /var/lib/mysql-files/
COPY Data/player_history.csv /var/lib/mysql-files/