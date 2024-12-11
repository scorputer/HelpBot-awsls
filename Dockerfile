# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Optionally set PYTHONPATH so that Python knows where to find src/app
# This ensures imports like from src.app import ... work without issues.
ENV PYTHONPATH="/app"

# Expose port 8000 for the Flask app
EXPOSE 8000

# Set an empty environment variable for OPENAI_API_KEY
# The actual key must be passed at runtime:
# docker run -e OPENAI_API_KEY=your_api_key helpbot:latest
ENV OPENAI_API_KEY=""

# Run the application
# Assuming HelpBot_awsls.py launches your Flask app on port 8000.
CMD ["python", "src/app/HelpBot_awsls.py"]
