# UTS Project

This project includes a Node.js application and a Flask application to manage and display travel information such as flights, trains, hotels, and attractions.

## Prerequisites

- Docker installed on your system
- Docker Hub account

## Setting Up the Node.js Application

### Dockerfile

Create a Dockerfile in the `node_app` directory:

```Dockerfile
# Use the official Node.js image from the Docker Hub
FROM node:16

# Create and change to the app directory
WORKDIR /usr/src/app

# Copy package.json and package-lock.json files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of your application files
COPY . .

# Expose the port your app runs on
EXPOSE 3000

# Command to run the app
CMD ["node", "server.js"]
```

### Building and Running the Docker Image

1. **Build the Docker image:**

```sh
docker build -t akdzan/node-service ./node_app
```

2. **Run the Docker container:**

```sh
docker run -p 3000:3000 -e PORT=3000 akdzan/node-service
```

3. **Push the Docker image to Docker Hub:**

```sh
docker login
docker tag akdzan/node-service akdzan/node-service:latest
docker push akdzan/node-service:latest
```

## Setting Up the Flask Application

### Dockerfile

Create a Dockerfile in the `flask_app` directory:

```Dockerfile
# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Install dependencies directly, using psycopg2-binary instead of psycopg2
RUN pip install --no-cache-dir Flask requests pymysql python-dotenv psycopg2-binary

# Copy the rest of your application files
COPY . .

# Expose the port your app runs on
EXPOSE 5000

# Command to run the app
CMD ["python", "Main.py"]
```

### Building and Running the Docker Image

1. **Build the Docker image:**

```sh
docker build -t akdzan/flask-service ./flask_app
```

2. **Run the Docker container:**

```sh
docker run -p 5000:5000 -e PORT=5000 akdzan/flask-service
```

3. **Push the Docker image to Docker Hub:**

```sh
docker login
docker tag akdzan/flask-service akdzan/flask-service:latest
docker push akdzan/flask-service:latest
```

## Running Both Applications

1. Ensure that both containers are running. You can verify by checking the logs or accessing the endpoints defined in each application.

2. Access the Node.js application at `http://localhost:3000` and the Flask application at `http://localhost:5000`.

## Using the Applications

### Node.js Endpoints

- `/flight`
- `/train`
- `/hotel`
- `/attractions`
- `/order`

### Flask Endpoints

- `/` - Main page
- `/admin` - Admin dashboard

### HTML Templates

The `index.html` and `admin.html` files are used for displaying the main page and the admin dashboard, respectively.

## Environment Variables

Make sure to set up your environment variables in a `.env` file as required by your applications. Here is an example:

```plaintext
API_KEY=FINALPROJECTEAI
```

Place the `.env` file in the root directory of each respective application.

## Conclusion

This project provides a complete setup for managing travel-related information using Node.js and Flask applications. The Dockerfiles allow you to containerize these applications for easy deployment and scalability.
