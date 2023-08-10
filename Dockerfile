# Use a lightweight base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that your FastAPI app will run on
EXPOSE 8000

# Start the FastAPI app using UVicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
