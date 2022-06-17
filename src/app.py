import logging
import sys
from graphs import histogram
from flask import Flask, request, jsonify

app = Flask(__name__, static_url_path='/', static_folder='./static')


@app.route('/')
def root():
    return app.send_static_file('index.html')


@app.route('/figure', methods=['POST'])
def createFigure():
    return histogram.createGraph(request.json)


if __name__ == '__main__':
    app.run()
