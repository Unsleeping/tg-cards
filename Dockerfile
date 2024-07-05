# Use an official Python runtime as a parent image
FROM python:3.9

# Set working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the files from the current directory to the container
COPY . .

# Run the bot when the container launches
CMD ["python", "main.py"]
