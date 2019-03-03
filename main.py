from flask import Flask
from flask import request
from data import Data
from urllib import parse


app = Flask(__name__)
cats_data = Data()


@app.route('/')
def index():
    return 'Cats Service welcomes you.' + '\n'


@app.route('/ping')
def ping():
    return 'Cats Service. Version 0.1' + '\n'


@app.route('/cat', methods=['POST'])
def cat():
    params_str = request.get_data().decode('utf-8').replace('"', '')[1:-1]

    if not params_str:
        return str(['Provide cat parameters, please.']) + '\n'

    params = dict(x.split(': ') for x in params_str.split(', '))

    return cats_data.add_cat(gross_params=params) + '\n'


@app.route('/cats')
def cats():
    return cats_data.get_cats(gross_params=request.args) + '\n'


if __name__ == '__main__':
    app.run(port=8080, threaded=True)
