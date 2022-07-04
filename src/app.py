# Config and routing
from flask import Flask, request
from config import Config

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
def create_figure():
    return Chart(app.config['UPLOAD_FOLDER'], request.json).generate()


@app.route('/upload', methods=['POST'])
def upload_file():
    return files.upload(request.files['file'])


@app.route('/api/browse', methods=['GET'])
def get_projects():
    return dict(result=files.list())


@app.route('/api/directory/<name>/', methods=['GET'])
def view_project(name):
    return files.access(name)


if __name__ == '__main__':
    app.run()
