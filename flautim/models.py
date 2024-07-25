from django.db import models
from utils import get_db_handle
from datetime import datetime
from pathlib import Path
import shutil

logs_collection = get_db_handle()['logs']

def log(object_type, id, message, details=None):
    #_id = str(ObjectId())
    logs_collection.insert_one(
        {
            #"_id": _id, 
            "timestamp": str(datetime.now()), "message": message, 
            "details" : details, "object":object_type, "object_id":id 
            }
        )


def configure_experiment_filesystem(base_path, id):
    experiments = get_db_handle()['experimento']
    projects = get_db_handle()['projeto']
    models = get_db_handle()['modelo']
    datasets = get_db_handle()['datasets']
    attachments = get_db_handle()['Attachments']

    experiment = experiments.find({"_id": id}).next()

    if experiment is None:
        raise Exception("Experiment ID does not exists")

    project = projects.find({"_id" : experiment["projectId"]}).next()

    _sigla = project["sigla"] if not project is None else experiment["acronym"] 

    base_folder = "{}/{}/{}/".format(base_path, _sigla, experiment["acronym"])

    check_dir(base_folder)

    for file_id in experiment["hyperparameterFile"]:
        file = attachments.find({"_id" : file_id})
        copy_file(file["path"], "{}{}".format(base_folder, file["name"]))

    for file_id in experiment["apiFile"]:
        file = attachments.find({"_id" : file_id})
        copy_file(file["path"], "{}{}".format(base_folder, file["name"]))

    model = models.find({"id" : experiment["modelId"]}).next()

    if not model is None:

        for file_id in model["archiveModel"]:
            file = attachments.find({"_id" : file_id})
            copy_file(file["path"], "{}model/{}".format(base_folder, file["name"]))

    dataset = datasets.find({"_id" : experiment["datasetId"]}).next()

    if not dataset is None:

        for file_id in dataset["files"]:
            file = attachments.find({"_id" : file_id})
            copy_file(file["path"], "{}data/{}".format(base_folder, file["name"]))


    return base_folder


def check_dir(path):
    p = Path(path)
    if not p.exists():
        p.mkdir(parents=True)
    # TODO: chown nobody:nogroup


def copy_file(path_from, path_to):
    pt = Path(path_to)
    if not pt.exists():
        pt.unlink()
    shutil.copy(path_from, path_to)