from django.db import models
from utils import get_db_handle

logs_collection = get_db_handle()['logs']
