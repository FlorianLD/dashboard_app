# Use an official Python runtime as a parent image
FROM python:3.12.3-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Make port 8050 available to the world outside this container
EXPOSE 8050

# Run app.py when the container launches
CMD ["python", "app.py"]