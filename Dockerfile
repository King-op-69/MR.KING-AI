# Use Python base image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy all files
COPY . /app

# Upgrade pip and setuptools
RUN pip install --upgrade pip setuptools

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]