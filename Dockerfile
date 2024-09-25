# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpython3-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expose the port that the app will run on
EXPOSE 8000

# Use gunicorn to run the Flask app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
