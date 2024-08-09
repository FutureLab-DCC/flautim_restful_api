from django.db import models
from utils import get_db_handle, read_config
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

config = read_config('filesystem')

BASE_PATH = config['base']
WEB_UPLOADS_FOLDER = config['web_uploads_folder']
REST_UPLOADS_FOLDER = config['rest_uploads_folder']

def map_paths(path):
    return path.replace(WEB_UPLOADS_FOLDER, REST_UPLOADS_FOLDER)

def get_job_name(id):
    experiments = get_db_handle()['experimento']
    experiment = experiments.find({"_id": id}).next()
    if experiment is None:
        raise Exception("Experiment ID does not exists")
    return experiment["acronym"].lower()


def update_experiment_status(id, status):
    filter = { '_id': id }
    newvalues = { "$set": { 'status': status } }
    experiments = get_db_handle()['experimento']
    experiments.update_one(filter, newvalues)


def configure_experiment_filesystem(id):
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

    base_folder = "{}/{}/{}/".format(BASE_PATH, _sigla, experiment["acronym"])
    output_folder = "{}{}/experiment_{}/".format(REST_UPLOADS_FOLDER, _sigla, experiment["acronym"])

    check_dir(base_folder, related_to=id)
    check_dir("{}{}".format(base_folder,"data"), related_to=id)
    check_dir("{}{}".format(base_folder,"models"), related_to=id)

    for file_id in experiment["hyperparameterFile"]:
        file = attachments.find({"_id" : file_id}).next()
        copy_file(map_paths(file["path"]), "{}{}".format(base_folder, file["name"]), related_to=id)

    for file_id in experiment["apiFile"]:
        file = attachments.find({"_id" : file_id}).next()
        copy_file(map_paths(file["path"]), "{}{}".format(base_folder, file["name"]), related_to=id)

    model = models.find({"_id" : experiment["modelId"]}).next()

    for file_id in model["archiveModel"]:
        file = attachments.find({"_id" : file_id}).next()
        copy_file(map_paths(file["path"]), "{}{}".format(base_folder, file["name"]), related_to=id)

    dataset = datasets.find({"_id" : experiment["datasetId"]}).next()

    for file_id in dataset["files"]:
        file = attachments.find({"_id" : file_id}).next()
        if file["extension"] == "py":
            copy_file(map_paths(file["path"]), "{}{}".format(base_folder, file["name"]), related_to=id)
        else:
            copy_file(map_paths(file["path"]), "{}data/{}".format(base_folder, file["name"]), related_to=id)


    return base_folder, output_folder, experiment["acronym"].lower()


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
    