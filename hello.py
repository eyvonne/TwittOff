# Import FLask package, flask makes app objects
from flask import Flask, render_template

# make the application
# create the flask webserver
app = Flask(__name__)
# dunder means it'll pull the name from the file

# routes determine location


@app.route('/')
# define a simple function
def home():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/classifier')
def classifier():
    return render_template('classifier.html')
