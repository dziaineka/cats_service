from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
    return 'Cats Service welcomes you.'


@app.route('/ping')
def ping():
    return 'Cats Service. Version 0.1'

if __name__ == '__main__':
    app.run()
