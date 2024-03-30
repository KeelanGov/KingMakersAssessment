# Recommender

The Recommender component is a recommendation system that utilizes machine learning techniques.

## Description

This component includes backend, frontend, and model modules required for the recommender system.

## Usage

To deploy the Recommender system, follow these steps:

1. Navigate to the `Recommender` directory.
2. Run `docker-compose build` to build the Docker containers.
3. Execute `docker-compose up` to run the system.
4. Wait for all containers to start up (This might take a while - so grab a coffee).
5. Once all containers are running, access the app via [http://localhost:8501/](http://localhost:8501/).

## NB: Configuration (On Mac) - (Not sure about other systems)

For docker-compose to be executed successfully, the following needs to be done:

   1. Configure shared paths from Docker -> Preferences... -> Resources -> File Sharing.
   2. Paths to share:
   - `path/to/this/cloned/repo/KingMakersAssessment`




[Back to Main](../README.md)
