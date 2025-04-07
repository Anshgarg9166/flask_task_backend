# Dockerfile
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy dependencies first (for caching)
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Set environment variable
ENV PYTHONUNBUFFERED=1

# Run the app
CMD ["flask", "run", "--host=0.0.0.0"]

ENV PYTHONUNBUFFERED=1
CMD ["flask", "run", "--host=0.0.0.0"]
