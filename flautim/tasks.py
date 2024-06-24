import os
from subprocess import PIPE, run
from celery import shared_task
from .models import log

def exec(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

@shared_task()
def runExperiment_task():
    #os.system("bash ./runExperiment.sh")
    command = "./runExperiment.sh"
    log("{} started".format(command))
    try:
        output = exec(command)
        log("{} finished: {}".format(command, output))
    except Exception as ex:
        log("{} finished with error: {}".format(command, repr(ex)))

@shared_task()
def statusExperiment_task():
    os.system("bash echo status")


@shared_task()
def stopExperiment_task():
    os.system("bash echo stop")


@shared_task()
def deleteExperiment_task():
    os.system("bash echo delete")