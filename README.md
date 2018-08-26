# BirdView AI Components

This repository contains the machine learning and AI components of BirdView

Current components under development:
* Facial Recognition
* Natural Language Understanding

To start:

flask run
 * if you don't have flask then run `pip3 install flask`

start your mongodb server: mongod

example to access the api through curl:

curl -F "file=@testimage.jpg" http://127.0.0.1:5000/nlu?text="Happy"

