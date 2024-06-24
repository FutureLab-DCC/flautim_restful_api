from django.shortcuts import render
from django.http import HttpResponse
from .models import logs_collection
import os
import subprocess
from poc.tasks import runExperiment_task, stopExperiment_task, statusExperiment_task, deleteExperiment_task

# Create your views here.

def index(request):
    logs = logs_collection.find()
    #print("Entrou")
    context = {
        "Logs" : logs
    }
    return render(request, 'index.html', context) #HttpResponse("<h1>App is runing ...</h1>") 

def runExperiment(request):
    runExperiment_task.delay()
    records = {
        "Call" : "Run"
    }
    logs_collection.insert_one(records)
    return render(request, "run.html", records)

def stopExperiment(request):
    stopExperiment_task.delay()
    records = {
        "Call" : "Stop"
    }
    logs_collection.insert_one(records)
    return render(request, "run.html", records)

def statusExperiment(request):
    statusExperiment_task.delay()
    records = {
        "Call" : "Status"
    }
    logs_collection.insert_one(records)
    return render(request, "run.html", records)

def deleteExperiment(request):
    deleteExperiment_task.delay()
    records = {
        "Call" : "Delete"
    }
    logs_collection.insert_one(records)
    return render(request, "run.html", records)