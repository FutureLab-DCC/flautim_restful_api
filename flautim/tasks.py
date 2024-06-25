import os
from subprocess import PIPE, run
from celery import shared_task
from .models import log

def exec(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

def task_base(id, command):
    log("experiment", id, "{} started".format(command))
    try:
        output = exec(command)
        log("experiment", id, "{} finished: {}".format(command, output))
    except Exception as ex:
        log("experiment", id, "{} finished with error: {}".format(command, repr(ex)))

@shared_task()
def runExperiment_task(id):
    task_base(id, "bash ./runExperiment.sh")
    

@shared_task()
def statusExperiment_task(id):
    task_base(id, "ls -la")


@shared_task()
def stopExperiment_task(id):
    task_base(id, "ps -ax")


@shared_task()
def deleteExperiment_task(id):
    task_base(id, "ls -la")