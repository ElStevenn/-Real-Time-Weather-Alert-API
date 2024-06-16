# Image Python 3.12 it's the image used for this program. Enjoy
FROM python:3.12-slim

# Define Workdir directory
WORKDIR /app

# Install Requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Port expose
EXPOSE 80
EXPOSE 5432

# Run Program
CMD []
