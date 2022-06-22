from chart import Chart
from flask import Flask, request

app = Flask(__name__, static_url_path='/', static_folder='./static')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/figure', methods=['POST'])
def createFigure():
    return Chart(request.json).generate()


if __name__ == '__main__':
    app.run()
