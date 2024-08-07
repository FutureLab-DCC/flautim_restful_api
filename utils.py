from pymongo import MongoClient
import yaml


def read_config(name):
    with open('config.yaml') as f:
        try: 
            cfg = yaml.safe_load(f)[name]
            return cfg
        except Exception as ex:
            raise ex


def get_db_handle():
    config = read_config('mongodb')
    client = MongoClient(host=config['host'],
                         port=int(config['port']),
                         username=config['username'],
                         password=config['password']
                         )
    db_handle = client[config['db']]
    return db_handle


