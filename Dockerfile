# Dockerfile

FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Environment variable to select the config
ENV FLASK_ENV=production
ENV FLASK_APP=app

CMD ["flask", "run", "--host=0.0.0.0"]
