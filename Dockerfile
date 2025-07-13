# Use a compatible base image with Python 3.10
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy rest of the app
COPY . .

# Run your backend
CMD ["python", "model_server.py"]
