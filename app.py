from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/figure', methods=['POST'])
def createFigure():
    print(request)
    return ''
    pass


if __name__ == '__main__':
    app.run(debug=True)
