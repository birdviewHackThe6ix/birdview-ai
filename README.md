# BirdView AI Components

This repository contains the machine learning and AI components of BirdView

Current components under development:
* Facial Recognition
* Natural Language Understanding

To start:

* `flask run` (if you don't have flask then run `pip3 install flask`)

* `mongod` to start your mongodb server

* `curl -F "file=@testimage.jpg" http://127.0.0.1:5000/nlu?text="Happy"` to access the endpoint

You will need to change the database name and collection that you are accessing in server.py

