FROM quay.io/devfile/python:slim

# By default, listen on port 8081
EXPOSE 8081/tcp
ENV FLASK_PORT=8081

# Create installation source
RUN mkdir -p /deploy/src
WORKDIR /deploy/
COPY src/requirements.txt ./src

# Install dependencies
RUN pip install -r ./src/requirements.txt

# Copy local src directory to working directory
COPY src ./src

# Set Python path
ENV PYTHONPATH=/deploy/src

EXPOSE 8080
ENV UPLOAD_DIR=/mnt
CMD gunicorn --workers 2 --bin 0.0.0.0:8080 app:app --log-level debug --timeout 600 --pythonpath '/deploy/src'