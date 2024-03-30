# Use an appropriate Python base image
FROM python:3.11

# Set the working directory
# WORKDIR .

# Copy the Streamlit app code and requirements file
COPY app.py .
COPY app_requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir --trusted-host pypi.org --trusted-host files.pythonhosted.org -r app_requirements.txt

# Expose the Streamlit port
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py"]