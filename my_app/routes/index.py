from my_app import app, cache
from flask import render_template


@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')