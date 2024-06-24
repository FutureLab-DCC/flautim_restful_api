from django.db import models
from utils import get_db_handle
from datetime import datetime

logs_collection = get_db_handle()['logs']

def log(message):
    logs_collection.insert_one({"timestamp": str(datetime.now()), "message": message })
