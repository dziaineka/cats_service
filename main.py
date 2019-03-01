from flask import Flask
from flask import request
from data import Data


app = Flask(__name__)
cats_data = Data()


@app.route('/')
def index():
    return 'Cats Service welcomes you.'


@app.route('/ping')
def ping():
    return 'Cats Service. Version 0.1'


@app.route('/cats')
def cats():
    return cats_data.get_cats(gross_params=request.args)


if __name__ == '__main__':
    app.run()
