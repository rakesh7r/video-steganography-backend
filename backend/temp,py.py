from flask import Flask,request,jsonify
from flask_cors import CORS
import cv2 as cv
import numpy as np
from PIL import Image

app = Flask(__name__)
CORS(app)





@app.route('/')
def default():
    return jsonify({'message':'Hello World'})

@app.route('/encode', methods = ['POST'])
def encode():
    # secret = request.json.get('secret')
    # file = request.json.get('file')
    secret = request.form['secret']
    file = request.form['file']
    print(secret,file)
    return jsonify({"secret":secret,"file":file})
  
@app.route('/<name>')
def greet(name):
    return jsonify({"name" : name})

if __name__ == '__main__':
    app.run(debug=True)