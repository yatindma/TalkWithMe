FROM python:3.9-slim-buster

# Create a non-root user for running the application
RUN adduser --disabled-password --gecos "" myuser

# Set the working directory to /app and make myuser the owner
WORKDIR /app
RUN chown myuser /app
USER myuser

# Install dependencies
COPY --chown=myuser:myuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY --chown=myuser:myuser . .

# Expose the port that the application will run on
EXPOSE 8000

# Start the application using Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
