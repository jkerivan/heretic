# Use an official Python runtime as the base image
FROM python:3.9-slim

# Install poetry
RUN pip install poetry

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies using poetry
RUN poetry install --no-root --no-interaction --no-ansi --no-dev

# Install psycopg2-binary separately
RUN pip install psycopg2-binary

# Make port 8000 available to the world outside this container
EXPOSE 8000


# Run app.py when the container launches
CMD ["poetry", "run", "start"]