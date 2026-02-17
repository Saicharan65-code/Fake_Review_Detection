# consumer/Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file and install dependencies
# This installs all necessary packages, including 'requests' for the API call 
# and 'psycopg2-binary' for the PostgreSQL database connection.
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the core application files
COPY config.py /app/
COPY dashboard_consumer.py /app/

# If you have a separate utils/logger.py file, copy that too
# If utils/logger.py is a utility file you created:
# COPY utils/logger.py /app/utils/

# The command to run the consumer is defined in docker-compose.yml 
# (although you could also define it here)
CMD ["python", "dashboard_consumer.py"]