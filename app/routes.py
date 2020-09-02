from flask import current_app as app


@app.route('/')
def index_page():
    return 'Welcome to the bar application.'
