from django.db import models
from utils import get_db_handle
from datetime import datetime
from django.bson.objectid import ObjectId

logs_collection = get_db_handle()['logs']

def log(object_type, id, message, details=None):
    _id = str(ObjectId())
    logs_collection.insert_one(
        {
            "_id": _id, "timestamp": str(datetime.now()), "message": message, 
            "details" : details, "object":object_type, "object_id":id 
            }
        )
