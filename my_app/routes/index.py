from my_app import app, cache
from flask import render_template


@app.route('/', methods=['GET'])
@cache.cached(timeout=50)
def index():
    return render_template('home.html')