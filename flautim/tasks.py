import os
from subprocess import PIPE, run
from celery import shared_task
from .models import log
from .k8s import job_create, job_stop, job_status


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
    raise NotImplementedError("This request is not implemented yet")