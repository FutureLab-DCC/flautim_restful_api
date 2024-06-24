import os
from subprocess import PIPE, run
from celery import shared_task
from .models import logs_collection


def exec(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

@shared_task()
def runExperiment_task():
    #os.system("bash ./runExperiment.sh")
    records = { "call" : "experiment/run/" }
    output = exec("./runExperiment.sh")
    records["description"] = str(output)
    logs_collection.insert_one(records)

@shared_task()
def statusExperiment_task():
    os.system("bash echo status")


@shared_task()
def stopExperiment_task():
    os.system("bash echo stop")


@shared_task()
def deleteExperiment_task():
    os.system("bash echo delete")