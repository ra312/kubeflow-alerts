import kfp
from kubernetes.client.models import V1EnvVar, V1ResourceRequirements, V1Volume, V1HostPathVolumeSource, V1SecretVolumeSource
from kcell_kfp_runners import HADOOP_VOLUMES
ALERT_IMAGE="artifactory.kraken.kcell.kz:6555/datalake-email-alert:latest"

@kfp.dsl.component
def send_email(name, title,  subject, body, args=[]):
    return kfp.dsl.ContainerOp(
        name=name,
        image=ALERT_IMAGE,
        pvolumes=HADOOP_VOLUMES,
        arguments=args,
        container_kwargs={
            "resources": k8s.V1ResourceRequirements(limits={"cpu": "1", "memory": "1Gi"}),
            "env": [
                k8s.V1EnvVar("NOTEBOOK", "/opt/" + notebook),
            ],
        },
        file_outputs={
            **outputs,
            "mlpipeline-ui-metadata": "/mlpipeline-ui-metadata.json"
        }
    )

