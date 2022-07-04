FROM quay.io/devfile/python:slim

# By default, listen on port 8081
EXPOSE 8081/tcp
ENV FLASK_PORT=8081

# Create installation source
RUN mkdir -p /deploy/app
WORKDIR /deploy/app
COPY src/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy local src directory to working directory
COPY src .
COPY gunicorn_config.py /deploy/

# Deploy application
COPY gunicorn_config.py .

# Set Python path
ENV PYTHONPATH=/deploy

EXPOSE 8080
CMD export UPLOAD_DIR="/mnt"
CMD gunicorn --workers 2 --bin 0.0.0.0:8080 app:app --log-level debug