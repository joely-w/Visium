# Config and routing
from flask import Flask, request
from src.config import Config

# Services
from chart import Chart
from files import Files

# Setup
app = Flask(__name__, static_url_path='/', static_folder='./static')
app.config.from_object(Config())

# Service instantiation
files = Files(app.config['UPLOAD_FOLDER'])


# Routes
@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/figure', methods=['POST'])
def createFigure():
    return Chart(request.json).generate()


@app.route('/upload', methods=['POST'])
def upload_file():
    return files.upload(request.files['file'])


if __name__ == '__main__':
    app.run()
