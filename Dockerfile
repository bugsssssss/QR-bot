# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment variables
# ENV BOT_TOKEN=your_bot_token_here

# Install build tools and development dependencies
RUN apt-get update && apt-get install -y build-essential && apt-get install -y libgl1-mesa-glx

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run bot.py when the container launches
CMD ["python3", "main.py"]
