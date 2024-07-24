from django.shortcuts import render
from django.http import JsonResponse
from .models import log, logs_collection, configure_experiment_filesystem
import os
import subprocess
from flautim.tasks import runExperiment_task, stopExperiment_task, statusExperiment_task, deleteExperiment_task, statusExperiment_synchronous

# Create your views here.

def index(request):
    logs = logs_collection.find()
    #print("Entrou")
    context = {
        "Logs" : logs
    }
    return render(request, 'index.html', context) 

def runExperiment(request, id):
    log("experiment", id, "Service call experiment/run/{}".format(id))
    try:
        runExperiment_task.delay(id)
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "error" , "details": repr(ex) }
        log("experiment", id, "experiment/run/{} failed: {}".format(id, repr(ex)))

    return JsonResponse(records)

def stopExperiment(request, id):
    log("experiment", id, "Service call experiment/stop/{}".format(id))
    try:
        stopExperiment_task.delay(id)
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "error" , "details": repr(ex) }
        log("experiment", id, "experiment/stop/{} failed: {}".format(id, repr(ex)))

    return JsonResponse(records)
    
def statusExperiment(request, id):
    log("experiment", id, "Service call experiment/status/{}".format(id))
    try:
        #statusExperiment_task.delay(id)
        status, ret, response = statusExperiment_synchronous(id)
        records = { "status": ret , "details": repr(response) }
    except Exception as ex:
        records = { "status": "error" , "details": repr(ex) }
        log("experiment", id, "experiment/status/{} failed: {}".format(id, repr(ex)))

    return JsonResponse(records)

def deleteExperiment(request, id):
    log("experiment", id, "Service call experiment/delete/{}".format(id))
    try:
        deleteExperiment_task.delay(id)
        records = { "status": "ok" }
    except Exception as ex:
        records = { "status": "error" , "details": repr(ex) }
        log("experiment", id, "experiment/delete/{} failed: {}".format(id, repr(ex)))

    return JsonResponse(records)
