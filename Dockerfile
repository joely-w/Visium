FROM quay.io/devfile/python:slim

# By default, listen on port 8081
EXPOSE 8081/tcp
ENV FLASK_PORT=8081

# Create installation source
RUN mkdir -p /deploy/src
WORKDIR /deploy/src
COPY src/requirements.txt ./
# Install dependencies
RUN pip install -r ./requirements.txt

# Copy local src directory to working directory
COPY src .

# Set Python path
ENV PYTHONPATH /deploy/src

EXPOSE 8080
ENV UPLOAD_DIR=/mnt

CMD gunicorn --workers 2 --bind 0.0.0.0:8080 app:app --log-level debug --timeout 600