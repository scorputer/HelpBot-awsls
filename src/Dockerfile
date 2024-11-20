# Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 8000 for the Flask app
EXPOSE 8000

# Declare the environment variable (without assigning a value)
ENV OPENAI_API_KEY=""

# Run the application
CMD ["python", "run.py"]
