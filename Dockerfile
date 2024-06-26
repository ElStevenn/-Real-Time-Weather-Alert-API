# Use the Python 3.12 slim image
FROM python:3.12-slim

# Define the working directory
WORKDIR /app

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app/ .

# Expose necessary ports
EXPOSE 8000
EXPOSE 80
EXPOSE 5432
EXPOSE 5000

# Command to run the application
CMD ["python3", "main.py"]
