import json

from flask import Flask
from flask import request
from data import Data
from urllib import parse
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["600 per minute"],
)

postgre_limit = limiter.shared_limit("600/minute", scope="postgre")

cats_data = Data()


@app.errorhandler(429)
def ratelimit_handler(e):
    return '429 Too Many Requests' + '\n'


@app.route('/')
@limiter.exempt
def index():
    return 'Cats Service welcomes you.' + '\n'


@app.route('/ping')
@limiter.exempt
def ping():
    return 'Cats Service. Version 0.1' + '\n'


@app.route('/cat', methods=['POST'])
@postgre_limit
def cat():
    return cats_data.add_cat(gross_params=request.get_data()) + '\n'


@app.route('/cats')
@postgre_limit
def cats():
    return cats_data.get_cats(gross_params=request.args) + '\n'


if __name__ == '__main__':
    app.run(port=8080, threaded=True)
