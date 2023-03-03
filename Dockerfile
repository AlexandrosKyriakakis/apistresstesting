# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any required Python packages
RUN pip3 install -r requirements.txt

# Define the command to run when the container starts
CMD [ "python3", "run.py" ]
