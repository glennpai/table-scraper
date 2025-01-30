# Use an official lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the script and dependencies into the image
COPY main.py .
COPY requirements.txt .
COPY .env .

# Install required Python libraries
RUN pip install -r requirements.txt

# Run the script
CMD ["python", "main.py"]
