# Config and routing
from flask import Flask, request, send_file

from src.charts import histogram, matrix
from src.config import Config
from src.uploads import Files

# Services

# Setup
app = Flask(__name__, static_url_path='/', static_folder='./static')
app.config.from_object(Config())

# Service instantiation
files = Files(app.config['UPLOAD_FOLDER'])


# Routes
@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/api/histogram', methods=['POST'])
def create_figure():
    return histogram.HistogramChart(app.config['UPLOAD_FOLDER'] + request.json).generate()


@app.route('/api/correlation_matrix', methods=['POST'])
def corr_matrix():
    return matrix.MatrixChart(app.config['UPLOAD_FOLDER'] + request.json).generate()


@app.route('/api/comparison', methods=['POST'])
def compare_matrices():
    print(request.json['path1'], request.json['path2'])
    path1 = f"{app.config['UPLOAD_FOLDER']}{request.json['project']}/{request.json['path1']}"
    path2 = f"{app.config['UPLOAD_FOLDER']}{request.json['project']}/{request.json['path2']}"
    return matrix.MatrixChart(path1, path2).generate()


@app.route('/upload', methods=['POST'])
def upload_file():
    return files.upload(request.files['file'])


@app.route('/api/browse', methods=['GET'])
def get_projects():
    return dict(result=files.list())


@app.route('/api/directory/<name>/', methods=['GET'])
def view_project(name: str):
    return files.access(name)


@app.route('/api/directory/<name>/pdf', methods=['GET'])
def view_pdf(name: str):
    filepath = files.pdf(name, request.args.get('filename'))
    return send_file(filepath)


if __name__ == '__main__':
    app.run()
