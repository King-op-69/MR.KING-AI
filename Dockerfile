# Use Python 3.10 slim (lightweight)
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy only requirements first for caching
COPY requirements.txt .

# Install dependencies first (caching benefit)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app files
COPY . .

# Set environment variables (optional but useful)
ENV BOT_USERNAME=_rip.king_
ENV BOT_PASSWORD=${BOT_PASSWORD}

# Run the bot
CMD ["python", "main.py"]
