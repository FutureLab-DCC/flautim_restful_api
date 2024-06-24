from django.shortcuts import render
from django.http import HttpResponse
from .models import logs_collection
import os
import subprocess
from poc.tasks import runExperiment_task

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
        "Test" : "Process requested"
    }
    #time_collection.insert_one(records)
    return render(request, "run.html", records)
