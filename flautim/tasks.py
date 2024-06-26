import os
from subprocess import PIPE, run
from celery import shared_task
from .models import log
from k8s import job_create, job_stop, job_status

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


def request_status(status):
    return "SUCCEED" if status else "FAILED"


@shared_task()
def runExperiment_task(id):
    try:
        status, response = job_create(id, id, 0, '/mnt')
        log("experiment_run", id, request_status(status), repr(response))
    except Exception as ex:
        log("experiment_run", id, request_status(False), repr(ex))
    

@shared_task()
def statusExperiment_task(id):
    try:
        status, response = job_status(id)
        log("experiment_status", id, request_status(status), repr(response))
    except Exception as ex:
        log("experiment_status", id, request_status(False), repr(ex))


@shared_task()
def stopExperiment_task(id):
    try:
        status, response = job_stop(id)
        log("experiment_delete", id, request_status(status), repr(response))
    except Exception as ex:
        log("experiment_delete", id, request_status(False), repr(ex))


@shared_task()
def deleteExperiment_task(id):
    task_base(id, "ls -la")