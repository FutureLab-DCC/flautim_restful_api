from pymongo import MongoClient
import yaml

def get_db_handle():
    with open('config.yaml') as f:
        try: 
            config = yaml.safe_load(f)['mongodb']
            client = MongoClient(host=config['host'],
                    port=int(config['port']),
                    username=config['username'],
                    password=config['password']
                     )
            db_handle = client[config['db']]
            return db_handle #, client
        except Exception as ex:
            raise ex
