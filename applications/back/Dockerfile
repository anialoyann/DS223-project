# Use Python 3.10 slim as the base image
FROM python:3.10-slim-bullseye

# Install system dependencies for Python packages
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libfreetype6-dev libpng-dev libjpeg-dev \
    libblas-dev liblapack-dev gfortran \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container to /app
WORKDIR /app

# Set environment variables to avoid .pyc files and ensure output is not buffered
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file into the container and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install uvicorn to run FastAPI
RUN pip install uvicorn

# Copy the entire project into the container
COPY . .

# Set the default command to run the FastAPI app using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
