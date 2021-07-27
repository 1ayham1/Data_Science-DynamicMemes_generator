import random
import os
import requests
from flask import Flask, render_template, request

from MemeEngine import MemeEngine
from QuoteEngine import Ingestor

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']


    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]

    return quotes, imgs


quotes, imgs = setup()

@app.route('/')
def meme_rand():
    """ Generate a random meme """

    img = random.choice(imgs)
    quote = random.choice(quotes)

    path = meme.make_meme(img, quote.author, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme 
    
    Help was obtained from knowledge Area
    """
    
    #Use requests to save the image from the image_url
    image_url = request.form['image_url']
    quote = request.form['quote', ""]
    author = request.form['author', ""]
    img_request = requests.get(image_url, allow_redirects=True)

    #form param to a temp local file.
    tmp = f'./temp/{random.randint(0, 1000000)}.jpg'

    with open(tmp, 'wb') as img_file:
        img_file.write(img_request.content)

    #generate a meme using this temp file.
    path = meme.make_meme(tmp, quote, author)
    
    #Remove the temporary saved image.
    os.remove(tmp)

    return render_template('meme.html', path=path)

if __name__ == "__main__":
    app.run()
