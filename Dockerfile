# Pull base image
FROM  python:3.11.4-slim-bullseye

# Set environment variable
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install ddependencies
COPY ./requirements.txt /code
COPY ./servers1.json .
RUN pip install -r requirements.txt
RUN pip install django-multiupload

# Add metadata to the image to describe that the container is listening on port 8000
EXPOSE 8000

# Copy project
COPY . .

#docker compose run web python3 manage.py migrate



# Install the dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Expose the port the app runs on (make sure this matches the port you're using)
EXPOSE 8001

# Define environment variable for Flask to run in production mode
ENV FLASK_ENV=production

# Start the Flask application
CMD ["python", "app.py"]