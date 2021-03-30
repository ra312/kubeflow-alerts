import kfp

def send_email(notebook, 
               limits={"cpu": "1", "memory": "1Gi"}, 
               outputs={}, args=[], 
               requests=None, image="artifactory.kraken.kcell.kz:6555/datalake-email-alert:latest"):
    if not requests:
        requests = limits
    return kfp.dsl.ContainerOp(
        name=notebook.split("/")[0],
        image=image,
        pvolumes=HADOOP_VOLUMES,
        arguments=args,
        container_kwargs={
            "resources": k8s.V1ResourceRequirements(limits=limits, requests=requests),
            "env": [
                k8s.V1EnvVar("NOTEBOOK", "/opt/" + notebook),
            ],
        },
        file_outputs={
            **outputs,
            "mlpipeline-ui-metadata": "/mlpipeline-ui-metadata.json",
            "executed-notebook": "/result.ipynb",
        },
    )

