# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in the code
RUN pip install Flask==2.0.3 pymysql==1.0.2 python-dotenv==0.19 werkzeug==2.0.3 confluent_kafka==1.7.0

# Make port 5432 available to the world outside this container
EXPOSE 5432

# Define environment variable
ENV FLASK_APP=config.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run", "--host=0.0.0.0", "--port=5432"]
