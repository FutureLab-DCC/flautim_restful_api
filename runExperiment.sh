#!/bin/sh
cd mnist-api-main/docker-image/mnist-experiment/
python run.py --IDexperiment Ex1 --user 0 --path data/ --dbuser futurelab --dbpw futurelab --dbport 27017

