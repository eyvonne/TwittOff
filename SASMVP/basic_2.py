from flask import Flask, render_template, request
import requests

app = Flask(__name__)

URL = 'https://dog.ceo/api/breeds/image/random'


def listBreeds():
    dog = requests.get('https://dog.ceo/api/breeds/list/all')
    breeds = dog.json()['message']
    allbreeds = []
    for key, value in breeds.items():
        if len(value) > 0:
            for sub in value:
                name = sub+' '+key
                allbreeds.append(name)
        else:
            allbreeds.append(key)
    return allbreeds


@app.route('/')
def home():
    title = "Look at this Dog"
    dogData = requests.get(URL)
    picture = dogData.json()['message']
    breeds = listBreeds()
    dogType = 'random dog'
    return render_template('home_2.html', picture=picture, title=title, breeds=breeds, dogType=dogType)


@app.route('/breeds')
def breeds():
    breeds = listBreeds()
    return render_template('breeds.html', breeds=allbreeds)


@app.route('/breed', methods=['POST'])
def breed():
    breed = request.values['breed']
    dogType = breed
    title = breed
    if len(breed.split()) == 2:
        one, two = breed.split()
        breed = two+'/'+one
    dog = requests.get('https://dog.ceo/api/breed/'+breed+'/images/random')
    picture = dog.json()['message']
    breeds = listBreeds()
    return render_template('home_2.html', picture=picture, title=title, breeds=breeds, dogType=dogType)


if __name__ == '__main__':
    app.run()
