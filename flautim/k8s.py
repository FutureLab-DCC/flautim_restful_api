from kubernetes import client, config
import yaml

def read_config(name):
    with open('config.yaml') as f:
        try: 
            cfg = yaml.safe_load(f)[name]
            return cfg
        except Exception as ex:
            raise ex
        
def get_k8s_config():
    return read_config('kubernetes')

def get_mongo_config():
    return read_config('mongodb')


def job_status(job_name):
    # Specify kubeconfig file
    cfg = get_k8s_config()
    kubeconfig_path = cfg['config_path']
    namespace = cfg['namespace']
    config.load_kube_config(config_file=kubeconfig_path)
    
    # Create an instance of the BatchV1Api
    batch_v1 = client.BatchV1Api()

    try:
        # Get the job details
        job = batch_v1.read_namespaced_job(name=job_name, namespace=namespace)
        
        # Extract and print job status details
        status = job.status

        return True, status

    except client.exceptions.ApiException as e:
        return False, repr(e)
    except Exception as e:
        return False, repr(e)
        
def job_stop(job_name):
    
    cfg = get_k8s_config()
    kubeconfig_path = cfg['config_path']
    namespace = cfg['namespace']

    # Load the specified kubeconfig file
    config.load_kube_config(config_file=kubeconfig_path)

    # Create an instance of the BatchV1Api
    batch_v1 = client.BatchV1Api()

    try:
        # Delete the job
        response = batch_v1.delete_namespaced_job(
            name=job_name,
            namespace=namespace,
            body=client.V1DeleteOptions(
                propagation_policy='Foreground',
                grace_period_seconds=0
            )
        )
        return True, response

    except client.exceptions.ApiException as e:
        return False, repr(e)
    except Exception as e:
        return False, repr(e)


def job_create(job_name, id_experiment, user, path):
    # Load the specified kubeconfig file
    cfg = get_k8s_config()
    kubeconfig_path = cfg['config_path']
    namespace = cfg['namespace']
    pvc = cfg['pvc']
    config.load_kube_config(config_file=kubeconfig_path)

    mongo_config = get_mongo_config()
    dbuser = mongo_config['username']
    dbpw = mongo_config['password']
    dbport = mongo_config['port']
    # Verify mongodb (ip)
    dbip = mongo_config['host']

    # Define the Job metadata
    metadata = client.V1ObjectMeta(name=job_name)
    
    # Define the container
    container = client.V1Container(
        name="mnist-trainer-job",
        image="sufex00/flautin:trainer-0.1",
        args=[
            "--IDexperiment", id_experiment,
            "--user", str(user),
            "--path", path,
            "--dbserver", dbip,
            "--dbuser", dbuser,
            "--dbpw", dbpw,
            "--dbport", str(dbport)
        ],
        image_pull_policy="Always",
        volume_mounts=[
            client.V1VolumeMount(
                name=pvc,
                mount_path="/mnt"
            )
        ]
    )
    
    # Define the volumes
    volume = client.V1Volume(
        name=pvc,
        persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
            claim_name="experiment-pvc"
        )
    )
    
    # Define the Pod template
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"job-type": "trainer"}),
        spec=client.V1PodSpec(
            restart_policy="Never",
            containers=[container],
            volumes=[volume]
        )
    )
    
    # Define the Job spec
    job_spec = client.V1JobSpec(template=template)
    
    # Define the Job
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=metadata,
        spec=job_spec
    )
    
    # Create an instance of the BatchV1Api
    batch_v1 = client.BatchV1Api()

    try:
        # Create the Job
        response = batch_v1.create_namespaced_job(
            body=job,
            namespace=namespace
        )
        return True, response

    except client.exceptions.ApiException as e:
        return False, repr(e)
    except Exception as e:
        return False, repr(e)



# get_status and delete variable
job_name = 'mnist-trainer-0'
data_path = '/mnt'
id_experiment = 'Ex1'

# Example usage
#job_response = create_job(
#    job_name=job_name,
#    id_experiment=id_experiment,
#    user=user,
#    path=data_path,
#    dbip = db_ip,
#    dbuser=db_user,
#    dbpw=db_user,
#    dbport=db_port,
#    kubeconfig_path=config_path
#)


#job_status = get_job_status(job_name, kubeconfig_path=config_path)
#delete_response = delete_job(job_name, kubeconfig_path=config_path)
