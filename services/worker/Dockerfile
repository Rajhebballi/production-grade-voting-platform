# Use Python image
FROM python:3.11-slim

# Working folder inside container
WORKDIR /app

# Copy dependency list
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy worker code
COPY app ./app

# Start worker
CMD ["python", "app/worker.py"]
