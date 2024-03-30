
[On mac]
For docker-compose to work, the following needs to be done
You can configure shared paths from Docker -> Preferences... -> Resources -> File Sharing.
paths to share:
- path/to/Recommender/Backend/jars/mysql-connector-j-8.3.0
- path/to/Recommender/spark-events
  
See https://docs.docker.com/desktop/mac
