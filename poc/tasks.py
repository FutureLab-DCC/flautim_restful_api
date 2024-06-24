import os
import subprocess
from celery import shared_task

@shared_task()
def runExperiment_task():
    os.system("bash ./runExperiment.sh")
