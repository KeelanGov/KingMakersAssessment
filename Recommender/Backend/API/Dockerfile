# Use an appropriate Python base image
FROM python:3.11

# Set the working directory
# WORKDIR /app

# Copy the API code and requirements file
COPY api.py .
COPY api_requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r api_requirements.txt

# Expose the API port
EXPOSE 5000

# Run the API
CMD ["python", "api.py"]