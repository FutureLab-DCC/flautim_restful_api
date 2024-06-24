import os
import subprocess
from celery import shared_task

@shared_task()
def runExperiment_task():
    os.system("bash ./runExperiment.sh")


@shared_task()
def stausExperiment_task():
    os.system("bash echo status")


@shared_task()
def stopExperiment_task():
    os.system("bash echo stop")


@shared_task()
def deleteExperiment_task():
    os.system("bash echo delete")