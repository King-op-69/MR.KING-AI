# Python 3.10 image use करें
FROM python:3.10

# Work directory set करें
WORKDIR /app

# Dependencies copy करें
COPY requirements.txt .

# Pip upgrade करें और dependencies install करें
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Main script copy करें
COPY . .

# App को run करें
CMD ["python", "main.py"]
