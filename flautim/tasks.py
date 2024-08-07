import os
from subprocess import PIPE, run
from celery import shared_task
from .models import log, configure_experiment_filesystem, get_job_name, update_experiment_status
from .k8s import job_create, job_stop, job_status


def request_status(status):
    return "SUCCEED" if status else "FAILED"


@shared_task()
def runExperiment_task(id):
    try:
        base_path, job_name = configure_experiment_filesystem(id)
        status, response = job_create(job_name, id, 0, base_path)
        log("experiment_run", id, request_status(status), repr(response))
    except Exception as ex:
        log("experiment_run", id, request_status(False), repr(ex))
    

def statusExperiment_synchronous(id):
    try:
        job_name = get_job_name(id)
        status, response = job_status(job_name)
        ret = 'error'
        if status:
            if response.active is not None and response.active > 0:
                ret = 'running'
            elif response.succeeded  is not None and response.suceeded > 0:
                ret = 'finished'
            elif response.failed  is not None and response.failed > 0:
                ret = 'error'

    except Exception as ex:
        status = False
        ret = 'error'
        response = repr(ex)
    
    return (status, ret, response)


@shared_task()
def stopExperiment_task(id):
    try:
        job_name = get_job_name(id)
        status, response = job_stop(job_name)
        update_experiment_status(id, "aborted")
        log("experiment_delete", id, request_status(status), repr(response))
    except Exception as ex:
        log("experiment_delete", id, request_status(False), repr(ex))


@shared_task()
def deleteExperiment_task(id):
    raise NotImplementedError("This request is not implemented yet")