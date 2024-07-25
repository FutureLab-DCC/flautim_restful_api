from django.db import models
from utils import get_db_handle
from datetime import datetime
from pathlib import Path
import shutil

logs_collection = get_db_handle()['logs']

def log(object_type, id, message, details=None):
    logs_collection.insert_one(
        {
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

    check_dir(base_folder, related_to=id)
    check_dir("{}{}".format(base_folder,"data"), related_to=id)
    check_dir("{}{}".format(base_folder,"models"), related_to=id)

    for file_id in experiment["hyperparameterFile"]:
        file = attachments.find({"_id" : file_id}).next()
        copy_file(file["path"], "{}{}".format(base_folder, file["name"]), related_to=id)

    for file_id in experiment["apiFile"]:
        file = attachments.find({"_id" : file_id}).next()
        copy_file(file["path"], "{}{}".format(base_folder, file["name"]), related_to=id)

    model = models.find({"_id" : experiment["modelId"]}).next()

    #if not model is None:

    for file_id in model["archiveModel"]:
        file = attachments.find({"_id" : file_id}).next()
        copy_file(file["path"], "{}{}".format(base_folder, file["name"]), related_to=id)

    dataset = datasets.find({"_id" : experiment["datasetId"]}).next()

    #if not dataset is None:

    for file_id in dataset["files"]:
        file = attachments.find({"_id" : file_id}).next()
        if file["extension"] == "py":
            copy_file(file["path"], "{}{}".format(base_folder, file["name"]), related_to=id)
        else:
            copy_file(file["path"], "{}data/{}".format(base_folder, file["name"]), related_to=id)


    return base_folder


def check_dir(path, related_to=None):
    try:
        p = Path(path)
        if not p.exists():
            p.mkdir(parents=True)
    except Exception as ex:
        log("filesystem.directory", related_to, "Unable to create directory {}".format(path), repr(ex))
        raise ex
    # TODO: chown nobody:nogroup


def copy_file(path_from, path_to, related_to=None):
    try:
        pt = Path(path_to)
        if pt.exists():
            pt.unlink()
        shutil.copy(path_from, path_to)
    except FileNotFoundError:
        log("filesystem.file", related_to, "File {} does not exists".format(path_from), repr(ex))
        raise ex
    
    except Exception as ex:
        log("filesystem.file", related_to, "Unable to copy file {} to {}".format(path_from, path_to), repr(ex))
        raise ex
    