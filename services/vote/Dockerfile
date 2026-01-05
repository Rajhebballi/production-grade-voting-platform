# Use Python image
FROM python:3.11-slim

# Set working folder inside container
WORKDIR /app

# Copy dependencies file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app/main.py"]
