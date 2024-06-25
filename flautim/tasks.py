import os
from subprocess import PIPE, run
from celery import shared_task
from .models import log

def exec(command):
    result = run(command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    return result.stdout

def task_base(command):
    log("{} started".format(command))
    try:
        output = exec(command)
        log("{} finished: {}".format(command, output))
    except Exception as ex:
        log("{} finished with error: {}".format(command, repr(ex)))

@shared_task()
def runExperiment_task():
    #os.system("bash ./runExperiment.sh")
    task_base("./runExperiment.sh")
    

@shared_task()
def statusExperiment_task():
    task_base("ls -la")


@shared_task()
def stopExperiment_task():
    task_base("ps -ax")


@shared_task()
def deleteExperiment_task():
    task_base("ls -la")