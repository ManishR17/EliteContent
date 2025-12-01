FROM python:3.12.6-slim

# Set working directory
WORKDIR /app

# Copy only requirements first (better caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire backend source
COPY . .

# Expose backend port
EXPOSE 8000

# Default: run main.py
# (Works for Flask or simple Python scripts)
CMD ["python", "main.py"]
