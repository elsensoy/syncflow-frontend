# Use an official Python runtime as a parent image
FROM python:3.9

# Install system dependencies required for a typical Python environment
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    gcc \
    libsndfile1 \
    portaudio19-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt with verbose output
RUN pip install --no-cache-dir -v -r requirements.txt

# Copy the rest of the application
COPY . /app

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for the Flask application
ENV FLASK_APP=app:create_app
ENV FLASK_RUN_HOST=0.0.0.0

# Run the Flask application using the app factory method
CMD ["flask", "run"]
