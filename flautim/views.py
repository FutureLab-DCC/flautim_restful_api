from django.shortcuts import render
from rest_framework.renderers import JSONRenderer, renderer_classes
from rest_framework.response import Response
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

@renderer_classes([JSONRenderer])
def runExperiment(request, id):
    log("experiment", id, "Service call experiment/run/{}".format(id))
    try:
        runExperiment_task.delay(id)
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "error" , "details": repr(ex) }
        log("experiment", id, "experiment/run/{} failed: {}".format(id, repr(ex)))

    return Response(records)

    #return render(request, "run.html", records)

def stopExperiment(request, id):
    log("experiment", id, "Service call experiment/stop/{}".format(id))
    try:
        stopExperiment_task.delay(id)
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "ok" }
        log("experiment", id, "experiment/stop/{} failed: {}".format(id, repr(ex)))

    return render(request, "run.html", records)
    
def statusExperiment(request, id):
    log("experiment", id, "Service call experiment/status/{}".format(id))
    try:
        statusExperiment_task.delay(id)
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "ok" }
        log("experiment", id, "experiment/status/{} failed: {}".format(id, repr(ex)))

    return render(request, "run.html", records)

def deleteExperiment(request, id):
    log("experiment", id, "Service call experiment/delete/{}".format(id))
    try:
        deleteExperiment_task.delay(id)
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "ok" }
        log("experiment", id, "experiment/delete/{} failed: {}".format(id, repr(ex)))

    return render(request, "run.html", records)