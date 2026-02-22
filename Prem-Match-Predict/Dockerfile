# Use a lightweight version of Python
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your Python script into the container
# MAKE SURE THIS MATCHES YOUR FILENAME EXACTLY!
COPY Prem_Match_Predictor.py .

# The command to run when the container starts
CMD ["python", "Prem_Match_Predictor.py"]