from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'a string'


@app.route('/puppy/<name>')
def puppy_name(name):
    return render_template('home_1.html', name=name)


@app.route('/addpuppy/<name>')
def addPuppy(name):
    letters = list(name)
    pup = {'pupname': name}
    puppies = ['ira', 'rudy', 'luna', 'eyve']
    return render_template('home_1.html', name=name, mylist=letters, mydict=pup,
                           puppies=puppies)


if __name__ == '__main__':
    app.run()
