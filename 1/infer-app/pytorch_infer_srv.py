#!/usr/bin/env python

import numpy as np
import torch, json
from torchvision import datasets, models, transforms

import redis

from PIL import Image
from flask import Flask, jsonify, abort, make_response, request

import hashlib
import os
import string
import random


class State:
  def __init__(self):
    self.labels = None
    self.imgTform = None
    self.image = None
    self.model = None
    self.cache = None

  def initDone(self):
      return self.labels != None

state = State()


# Load and init model
def init_inference():
    print(">>> Initialization started...")

    # redis_url = os.environ['REDIS_URL']
    # print(os.environ['REDIS_HOST'])
    # print(os.environ['REDIS_PORT'])
    # redis_url = "redis://6379"
    # redis_url = "localhost"
    # state.cache = redis.Redis(host=redis_url)

    redis_host = os.environ['REDIS_HOST']
    redis_port = os.environ['REDIS_PORT']
    state.cache = redis.Redis(host=redis_host, port=redis_port)
    state.cache.ping() 
    print(">>> Connected to redis...")

    state.imgTform = transforms.Compose([transforms.Resize((224, 224)), transforms.ToTensor()])
    state.model = models.mobilenet_v3_small(pretrained=True)
    state.model.eval()
    state.labels = models.MobileNet_V3_Small_Weights.DEFAULT.meta["categories"]
    print(">>> Loaded model...")

    print(">>> Initialization finished.")


def infer(file):
    # Load the image
    image = Image.open(file, formats = ['JPEG', 'PNG'])
    if not image:
        return "Could not read image. Supported formats: JPEG, PNG"
    
    # Check cache
    hash = hashlib.sha256(image.tobytes()).hexdigest()
    cache_resp = state.cache.get(hash)
    if cache_resp:
        print(">>> Found in cache")
        return "Found in cache - " + cache_resp.decode("utf-8")   

    # Now apply the transformation, expand the batch dimension
    image = state.imgTform(image).unsqueeze(0)
    if image is None:
        return "Could not process data. Try another image"

    # Get the 1000-dimensional model output
    out = state.model(image)
    if out is None:
        return "Could not process data. Try another image"

    # Find the predicted class
    result = state.labels[out.argmax()]
    
    # Update cache
    print(">>> Not found in cache")
    state.cache.set(hash, result)

    return "Not found in cache - " + result 


# Flask server
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = './uploads'


@app.route('/infer/', methods = ['POST'])
def infer_request_handler():
    if not state.initDone():
        return jsonify("Server initialization is in progress. Try later")
    
    try:
        if request.method == 'POST':
            file = request.files['file']
            if file:
                result = infer(file)
                print(">>> Result: " + result)
                response = jsonify(result)
                response.headers.add("Access-Control-Allow-Origin", "*")
                return response
    except Exception as e:
        print(e)
        return jsonify("Internal Error")

    return jsonify("Bad Request")


if __name__ == '__main__':
    init_inference()
    app.run(host='0.0.0.0', port=50000, debug=False)
