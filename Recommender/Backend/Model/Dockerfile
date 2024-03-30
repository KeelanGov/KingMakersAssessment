# Use an appropriate Python base image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY model_requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --retries 3 --timeout 300 --trusted-host pypi.org --trusted-host files.pythonhosted.org -r model_requirements.txt

# Install Java 11 and procps (provides the "ps" command)
RUN apt-get update && \
    apt-get install -y openjdk-11-jdk procps && \
    apt-get clean

# Set the JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64

# Copy the recommender script
COPY recommender.py .

# Run the recommender script
CMD ["spark-submit", "--master", "local[*]", "--jars", "/app/jars/mysql-connector-j-8.3.0.jar", "recommender.py"]