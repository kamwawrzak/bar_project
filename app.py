from flask import Flask


app = Flask(__name__)


@app.route('/')
def index_page():
    return 'Welcome to the bar application.'


@app.route('/v1/register/')
def register_user():
    pass


if __name__ == '__main__':
    app.run(debug=True)
