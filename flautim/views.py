from django.shortcuts import render
from django.http import HttpResponse
from .models import log, logs_collection
import os
import subprocess
from flautim.tasks import runExperiment_task, stopExperiment_task, statusExperiment_task, deleteExperiment_task

# Create your views here.

def index(request):
    logs = logs_collection.find()
    #print("Entrou")
    context = {
        "Logs" : logs
    }
    return render(request, 'index.html', context) 

def runExperiment(request):
    log("Service call experiment/run/")
    try:
        runExperiment_task.delay()
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "ok" }
        log("experiment/run/ failed: {}".format(repr(ex)))

    return render(request, "run.html", records)

def stopExperiment(request):
    log("Service call experiment/stop/")
    try:
        stopExperiment_task.delay()
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "ok" }
        log("experiment/stop/ failed: {}".format(repr(ex)))

    return render(request, "run.html", records)
    
def statusExperiment(request):
    log("Service call experiment/status/")
    try:
        statusExperiment_task.delay()
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "ok" }
        log("experiment/status/ failed: {}".format(repr(ex)))

    return render(request, "run.html", records)

def deleteExperiment(request):
    log("Service call experiment/delete/")
    try:
        deleteExperiment_task.delay()
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "ok" }
        log("experiment/delete/ failed: {}".format(repr(ex)))

    return render(request, "run.html", records)