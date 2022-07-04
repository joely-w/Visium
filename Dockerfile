FROM mpsorg/sass-compiler AS sass-compiler
WORKDIR /deploy/app
RUN mkdir -p /deploy/app

COPY src .
RUN sass /src/stylsheets:/deploy/app/stylesheets

FROM quay.io/devfile/python:slim

# By default, listen on port 8081
EXPOSE 8081/tcp
ENV FLASK_PORT=8081

# Create installation source
WORKDIR /deploy/app
COPY src/requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy local src directory to working directory
COPY gunicorn_config.py /deploy/

# Deploy application
COPY gunicorn_config.py .

# Set Python path and upload directory
ENV PYTHONPATH=/deploy
ENV UPLOAD_DIR=/mnt
EXPOSE 8080

CMD gunicorn --workers 2 --bin 0.0.0.0:8080 app:app --log-level debug