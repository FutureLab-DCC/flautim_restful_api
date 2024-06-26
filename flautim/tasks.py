import os
from subprocess import PIPE, run
from celery import shared_task
from .models import log
from .k8s import create_job

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
    #task_base(id, "ls -la")
    try:
        status, response = create_job(id, id, 0, '/mnt')
        if status:
            log("experiment", id, "Task OK: {}".format(response))
        else:
            log("experiment", id, "Task FAILED: {}".format(response))
    except Exception as ex:
        log("experiment", id, "Task FAILED: {}".format(repr(ex)))



@shared_task()
def stopExperiment_task(id):
    task_base(id, "ps -ax")


@shared_task()
def deleteExperiment_task(id):
    task_base(id, "ls -la")